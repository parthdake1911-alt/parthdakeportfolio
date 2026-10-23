"""Make lighter copies of the prototype files for the hosted site.

Originals are never modified. Optimized copies go to optimized/protos/.
- Embedded JPEG/PNG images -> WebP (alpha kept), oversized images resized to their display size.
- Customer Smile: duplicate images stored once, screens stored as plain text (no second base64 layer).
- jQuery loaded from the site's own assets/ folder instead of a CDN.
"""
import base64, io, json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'optimized', 'protos')
os.makedirs(OUT, exist_ok=True)
JQ_LOCAL = '../assets/jquery-3.7.1.min.js'
DATA = re.compile(r'data:(image/(?:png|jpeg|jpg|webp));base64,([A-Za-z0-9+/=]+)')

def shrink(b64, mime, maxdim=None, q=80, min_kb=8, force=False):
    """Return (mime, b64) for a smaller WebP version, or the original if not worth it."""
    raw = base64.b64decode(b64)
    if len(raw) < min_kb * 1024 and not force:
        return mime, b64
    im = Image.open(io.BytesIO(raw))
    im.load()
    alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
    im = im.convert('RGBA' if alpha else 'RGB')
    if maxdim and max(im.size) > maxdim:
        s = maxdim / max(im.size)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=q, method=6, alpha_quality=90)
    new = buf.getvalue()
    if len(new) < len(raw) * 0.92 or (maxdim and force):
        return 'image/webp', base64.b64encode(new).decode()
    return mime, b64

def sub_images(html, rule):
    def f(m):
        mime, b64 = m.group(1), m.group(2)
        im = Image.open(io.BytesIO(base64.b64decode(b64)))
        maxdim, q = rule(im, mime, len(b64))
        if maxdim is None and q is None:
            return m.group(0)
        mime2, b2 = shrink(b64, mime, maxdim, q or 80)
        return f'data:{mime2};base64,{b2}'
    return DATA.sub(f, html)

def report(name, before, after):
    print(f'{name:28s} {before/1e6:5.2f} MB -> {after/1e6:5.2f} MB')

def write(name, html, before):
    open(os.path.join(OUT, name), 'w').write(html)
    report(name, before, len(html.encode()))

# ---------- ICA: photos to WebP, nothing larger than 1920 ----------
src = open(os.path.join(ROOT, 'ica/src/ica.html')).read()
write('ica.html', sub_images(src, lambda im, m, n: (1920, 80)), len(src.encode()))

# ---------- Ellenbarrie: service illustrations shown at <=210 units -> 600 px; local jQuery ----------
src = open(os.path.join(ROOT, 'ellen/src/redesign.html')).read()
def ellen_rule(im, m, n):
    if im.size == (1254, 1254):
        return 600, 82
    return (None, 80) if n > 120_000 else (None, None)
h = sub_images(src, ellen_rule)
h = re.sub(r'src="https://code\.jquery\.com/jquery-3\.7\.1\.min\.js"[^>]*>', f'src="{JQ_LOCAL}">', h)
assert 'code.jquery.com' not in h
write('ellenbarrie.html', h, len(src.encode()))

# ---------- Anchor ----------
src = open(os.path.join(ROOT, 'anchor/src/anchor.html')).read()
write('anchor.html', sub_images(src, lambda im, m, n: (None, 82)), len(src.encode()))

# ---------- AMIN: bundled app; shrink the 4096 px background inside the manifest ----------
src = open(os.path.join(ROOT, 'amin/src/portal.html')).read()
mm = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', src, re.S)
man = json.loads(mm.group(2))
for k, v in man.items():
    if v.get('mime') in ('image/jpeg', 'image/png') and not v.get('compressed'):
        mime2, b2 = shrink(v['data'], v['mime'], maxdim=2560, q=80)
        v['mime'], v['data'] = mime2, b2
h = src[:mm.start(2)] + json.dumps(man, separators=(',', ':')).replace('</', '<\\/') + src[mm.end(2):]
write('amin.html', h, len(src.encode()))

# ---------- Customer Smile: dedupe images, plain-text screens, local jQuery ----------
src = open(os.path.join(ROOT, 'tata/src/mcs.html')).read()
sm = re.search(r'(<script id="screens" type="application/json">)(.*?)(</script>)', src, re.S)
screens = {k: base64.b64decode(v).decode() for k, v in json.loads(sm.group(2)).items()}
screens = {'home': screens['home']}   # the portfolio shows the homepage only; other screens aren't shipped
# Keep the bottom nav and header pinned on every device: the page scrolls inside <body> rather than the
# document, so the screen's own height never grows (iOS Safari otherwise stretches the frame and the
# fixed nav scrolls away with it). window.scrollY / scrollTo / 'scroll' events are forwarded to <body>.
PIN = """<style id="pin-shell">html{height:100%;overflow:hidden}body{height:100%;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}</style>
<script>(function(){var b=function(){return document.body};
Object.defineProperty(window,'scrollY',{get:function(){return b()?b().scrollTop:0}});
Object.defineProperty(window,'pageYOffset',{get:function(){return b()?b().scrollTop:0}});
window.scrollTo=function(x,y){var o=(typeof x==='object')?x:{left:x,top:y};if(b())b().scrollTo(o)};
window.scrollBy=function(x,y){var o=(typeof x==='object')?x:{left:x,top:y};if(b())b().scrollBy(o)};
document.addEventListener('DOMContentLoaded',function(){b().addEventListener('scroll',function(){window.dispatchEvent(new Event('scroll'))},{passive:true})});})();</script>"""
screens['home'] = screens['home'].replace('</head>', PIN + '\n</head>', 1)
assert 'pin-shell' in screens['home']
table, index = [], {}
def tata_img(m):
    mime, b64 = m.group(1), m.group(2)
    if b64 not in index:
        im = Image.open(io.BytesIO(base64.b64decode(b64)))
        # phone screens are 393 css px wide; 900 px covers 2x displays
        mime2, b2 = shrink(b64, mime, maxdim=900, q=80)
        index[b64] = len(table); table.append(f'data:{mime2};base64,{b2}')
    return f'__I{index[b64]}__'
DATA_ANY = re.compile(r'data:(image/(?:png|jpeg|jpg|webp));base64,([A-Za-z0-9+/=]+)')
for k in screens:
    h = DATA_ANY.sub(tata_img, screens[k])
    h = h.replace('https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js', JQ_LOCAL)
    h = re.sub(r'\s+integrity="[^"]*"', '', h) if JQ_LOCAL in h else h
    assert 'cdnjs.cloudflare.com/ajax/libs/jquery' not in h
    screens[k] = h
def js_json(o):
    return json.dumps(o, separators=(',', ':')).replace('</', '<\\/').replace('<!--', '<\\u0021--')
h = src[:sm.start()] + '<script id="imgs" type="application/json">' + js_json(table) + '</script>\n' \
    + sm.group(1) + js_json(screens) + sm.group(3) + src[sm.end():]
old = "var SRC=JSON.parse(document.getElementById('screens').textContent), CACHE={};\n  function html(k){ if(!CACHE[k]){ var b=atob(SRC[k]), u=new Uint8Array(b.length); for(var i=0;i<b.length;i++) u[i]=b.charCodeAt(i); CACHE[k]=new TextDecoder().decode(u); } return CACHE[k]; }"
new = "var SRC=JSON.parse(document.getElementById('screens').textContent), IM=JSON.parse(document.getElementById('imgs').textContent), CACHE={};\n  function html(k){ if(!CACHE[k]){ CACHE[k]=SRC[k].replace(/__I(\\d+)__/g,function(m,i){ return IM[+i]; }); } return CACHE[k]; }"
assert h.count(old) == 1, 'Customer Smile loader changed'
h = h.replace(old, new)
# the phone frame always fits the visible screen (in-app browsers and Safari toolbars included), so the bottom nav is never cut off
dev_old = "@media (max-width:392px){ body{display:block} .device{width:100%;height:100vh;height:100dvh} }"
assert h.count(dev_old) == 1, 'device CSS changed'
h = h.replace(dev_old, "@media (max-width:392px){ body{display:block} .device{width:100%} }\n  .device{height:min(852px,100vh);height:min(852px,100dvh);max-width:100vw}\n  @media (max-width:500px){ body{display:block} .device{width:100%} }")
# homepage only: anything that would open another screen shows a short note instead
for fn in ('function tab(k){', 'function push(k){'):
    assert h.count(fn) == 1, fn
    h = h.replace(fn, fn + " if(k!=='home'){ toast('This preview shows the homepage only'); return; }")
print(f'  Customer Smile: {len(table)} unique images')
write('tatapower.html', h, len(src.encode()))

# ---------- Casagrand: embedded photos -> separate WebP files (stored once, cached by the browser) ----------
import hashlib, shutil
src = open(os.path.join(ROOT, 'casa/src/casagrand.html'), encoding='utf-8').read()
CG = os.path.join(OUT, 'casagrand_proto')
shutil.rmtree(CG, ignore_errors=True); os.makedirs(CG)
done = {}
def cg_img(m):
    mime, b64 = m.group(1), m.group(2)
    if b64 not in done:
        im = Image.open(io.BytesIO(base64.b64decode(b64))); im.load()
        alpha = im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info)
        im = im.convert('RGBA' if alpha else 'RGB')
        if im.width > 1920:
            im = im.resize((1920, round(im.height * 1920 / im.width)), Image.LANCZOS)
        name = 'cg-' + hashlib.md5(b64.encode()).hexdigest()[:10] + '.webp'
        im.save(os.path.join(CG, name), 'WEBP', quality=80, method=6, alpha_quality=90)
        done[b64] = 'proto/' + name
    return done[b64]
h = DATA_ANY.sub(cg_img, src)
size = sum(os.path.getsize(os.path.join(CG, f)) for f in os.listdir(CG))
print(f'  Casagrand: {len(done)} unique images, {size/1e6:.2f} MB as files')
write('casagrand.html', h, len(src.encode()))
