"""Build the hosted, multi-file portfolio into ./site (the folder you upload to Netlify).

site/
  index.html            homepage                    404.html   not-found page
  _headers              Netlify caching rules       assets/    shared scripts (jQuery for two prototypes)
  images/  media/  resume/
  amin/ anchor/ ultratech/ ellenbarrie/ ica/ tatapower/   one folder per case study:
        index.html, img/*, prototype.html (where there is one)

Run optimize_prototypes.py first (build_all.py does everything in order).
"""
import io, json, os, re, shutil, subprocess
from PIL import Image

H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, 'site')
OPT = os.path.join(H, 'optimized')
shutil.rmtree(OUT, ignore_errors=True)
for d in ['resume', 'images/cards', 'media', 'assets', 'amin/img', 'anchor/img', 'ultratech/img', 'ellenbarrie/img', 'ica/img', 'tatapower/img', 'casagrand/img', 'casagrand/proto']:
    os.makedirs(f'{OUT}/{d}', exist_ok=True)

def cp(src, dst):
    shutil.copy(src, f'{OUT}/{dst}')
    return dst

def save_webp(src, dst, max_h=None, q=88):
    im = Image.open(src)
    im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') else 'RGB')
    if max_h and im.height > max_h:
        im = im.resize((round(im.width * max_h / im.height), max_h), Image.LANCZOS)
    im.save(f'{OUT}/{dst}', 'WEBP', quality=q, method=6, alpha_quality=95)
    return dst

# ---------- shared + homepage assets ----------
save_webp(f'{H}/cards/logo.png', 'images/logo.webp', max_h=160)          # shown at 40 px tall
covers = {}
for k in ['amin', 'ultratech', 'tata', 'ica', 'ellenbarrie', 'anchor', 'casagrand', 'sp']:
    src = f'{OPT}/images/cards/{k}.webp' if os.path.exists(f'{OPT}/images/cards/{k}.webp') else f'{H}/cards/{k}.webp'
    covers[k] = cp(src, f'images/cards/{k}.webp')
    cp(f'{OPT}/images/cards/{k}.avif', f'images/cards/{k}.avif')
for k in ['convo_crop', 'convo_full', 'bcw']:
    cp(f'{H}/cards/{k}.webp', f'images/{k}.webp')
    cp(f'{OPT}/images/{k}.avif', f'images/{k}.avif')
# hero: small client logos for the "Hi, I'm" pill
HL = {}
for k, f in [('TATA', 'tata.png'), ('ICA', 'ica.png'), ('CASA', 'casagrand.png'), ('ULTRA', 'ultratech.png')]:
    HL[k] = save_webp(f'{H}/logos/{f}', f'images/hl-{k.lower()}.webp', max_h=96, q=90)
cp(f'{OPT}/resume/Parth-Dake-Resume.pdf', 'resume/Parth-Dake-Resume.pdf')
cp(f'{OPT}/jquery-3.7.1.min.js', 'assets/jquery-3.7.1.min.js')

# ---------- homepage ----------
t = open(f'{H}/template.html').read()
pages = {'case': 'amin/', 'proto': 'amin/prototype.html', 'anchorCase': 'anchor/', 'anchorProto': 'anchor/prototype.html',
         'ultraCase': 'ultratech/', 'ellenCase': 'ellenbarrie/', 'ellenProto': 'ellenbarrie/prototype.html',
         'icaCase': 'ica/', 'icaProto': 'ica/prototype.html', 'tataCase': 'tatapower/', 'tataProto': 'tatapower/prototype.html',
         'casaCase': 'casagrand/', 'casaProto': 'casagrand/prototype.html'}
rep = {
    '{{IMAGES}}': json.dumps(covers), '{{HM_TATA}}': covers['tata'], '{{HM_CASA}}': covers['casagrand'],
    **{'{{HL_%s}}' % k: v for k, v in HL.items()},
    '{{CONVOFULL_AVIF}}': 'images/convo_full.avif', '{{CONVOFULL}}': 'images/convo_full.webp',
    '{{CONVO_AVIF}}': 'images/convo_crop.avif', '{{CONVO}}': 'images/convo_crop.webp',
    '{{BCW_AVIF}}': 'images/bcw.avif', '{{BCW}}': 'images/bcw.webp',
    '{{LOGO}}': 'images/logo.webp', '{{PAGES}}': json.dumps(pages),
}
for k, v in rep.items():
    assert k in t, k
    t = t.replace(k, v)
for a, b in [('amin', 'amin'), ('anchor', 'anchor'), ('ultratech', 'ultratech'), ('ellenbarrie', 'ellenbarrie'), ('ica', 'ica'), ('tata', 'tatapower'), ('casagrand', 'casagrand')]:
    t = t.replace(f"href: '{a}-case-study.html'", f"href: '{b}/'")
old = "f.srcdoc = P[key];"
assert old in t
t = t.replace(old, "f.src = P[key];")                    # layers load a real URL
assert '{{' not in re.sub(r'<script>window.__PAGES.*?</script>', '', t), 'unfilled placeholder in homepage'
open(f'{OUT}/index.html', 'w').write(t)

# ---------- case-study helpers ----------
PAGE_CSS = """
  :where(img[width][height]) { height: auto; }
  .client-logo { display: flex; align-items: center; margin-bottom: clamp(18px, 2.4vw, 28px); }
  .client-logo img { height: var(--lh, 44px); width: auto; max-width: min(100%, 420px); object-fit: contain; display: block; }
  @media (max-width: 640px) { .client-logo img { height: calc(var(--lh, 44px) * .78); } }
"""
def add_logo(p, folder, logo, alt, h):
    ext = os.path.splitext(logo)[1]
    if ext == '.png':                                      # transparent PNG -> WebP keeps transparency, much smaller
        dst = save_webp(logo, f'{folder}/img/client-logo.webp', max_h=h * 3, q=90); ext = '.webp'
    else:
        dst = cp(logo, f'{folder}/img/client-logo{ext}')
    mark = '<a href="portfolio-hero.html#work" class="kicker"'
    i = p.index('id="hero"'); j = p.index(mark, i)
    k = p.rindex('\n', 0, j) + 1; indent = p[k:j]
    tag = f'<div class="client-logo rv" style="--lh:{h}px"><img src="img/client-logo{ext}" alt="{alt}"></div>\n' + indent
    return p[:j] + tag + p[j:]

def add_dims(p, folder):
    """Give every local <img> its real width/height so the page doesn't jump while images load."""
    def f(m):
        tag, src = m.group(0), m.group(1)
        if ' width=' in tag or src.startswith(('data:', 'http')):
            return tag
        path = os.path.normpath(os.path.join(OUT, folder, src))
        if not os.path.isfile(path) or path.endswith('.svg'):
            if path.endswith('.svg'):
                vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(path).read())
                if vb: return tag.replace('<img ', f'<img width="{round(float(vb.group(1)))}" height="{round(float(vb.group(2)))}" ', 1)
            return tag
        w, h = Image.open(path).size
        tag = tag.replace('<img ', f'<img width="{w}" height="{h}" ', 1)
        if 'decoding=' not in tag:
            tag = tag.replace('<img ', '<img decoding="async" ', 1)
        return tag
    return re.sub(r'<img [^>]*?src="([^"]+)"[^>]*>', f, p)

def case_page(src_html, folder, img_dir, extra=None, logo=None, alt='', h=44):
    p = open(src_html).read()
    if logo:
        p = add_logo(p, folder, logo, alt, h)
    p = p.replace('</style>', PAGE_CSS + '</style>', 1)
    p = p.replace('<link rel="preconnect" href="https://fonts.googleapis.com">',
                  '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', 1)
    p = p.replace('href="portfolio-hero.html"', 'href="../"').replace('href="portfolio-hero.html#', 'href="../#')
    p = p.replace("href.startsWith('portfolio-hero.html')", "href.startsWith('../')")
    for k, v in (extra or {}).items():
        assert k in p, (folder, k[:60])
        p = p.replace(k, v)
    def sub(m):
        k = m.group(1)
        if k == 'LOGO':
            return '../images/logo.webp'
        src = f'{img_dir}/{k}.webp'
        assert os.path.exists(src), src
        return cp(src, f'{folder}/img/{k}.webp').split('/', 1)[1]
    p = re.sub(r'\{\{([A-Za-z0-9_]+)\}\}', sub, p)
    p = add_dims(p, folder)
    assert 'portfolio-hero.html' not in p, folder
    open(f'{OUT}/{folder}/index.html', 'w').write(p)
    return p

L = f'{H}/logos'
PROTO = f'{OPT}/protos'

# ---------- AMIN ----------
cp(f'{H}/amin/out/poster.jpg', 'amin/img/poster.jpg')
cp(f'{H}/amin/out/amin-walkthrough.mp4', 'amin/walkthrough.mp4')        # H.264 MP4 plays in every current browser
cp(f'{PROTO}/amin.html', 'amin/prototype.html')
amin = case_page(f'{H}/amin/case.html', 'amin', f'{H}/amin/out', logo=f'{L}/amin.png', alt='AMIN Worldwide logo', h=44, extra={
    '{{POSTER}}': 'img/poster.jpg', '<source src="{{VIDEOSRC}}" type="video/mp4">': '<source src="walkthrough.mp4" type="video/mp4">',
    'href="amin-prototype.html" target="_blank"': 'href="prototype.html" data-proto="proto" target="_blank"',
    "else if (href === 'amin-prototype.html') { e.preventDefault(); parent.postMessage({ pd: 'proto' }, '*'); }":
    "else if (a.dataset.proto) { e.preventDefault(); parent.postMessage({ pd: 'proto', key: a.dataset.proto }, '*'); }",
})
assert 'amin-prototype.html' not in amin and 'a.dataset.proto' in amin

# ---------- Anchor ----------
cp(f'{PROTO}/anchor.html', 'anchor/prototype.html')
case_page(f'{H}/anchor/case.html', 'anchor', f'{H}/anchor/out', logo=f'{L}/anchor.svg', alt='Anchor logo', h=66,
          extra={'href="anchor-prototype.html"': 'href="prototype.html"'})

# ---------- UltraTech (confidential: three cropped glimpses only, no prototype) ----------
case_page(f'{H}/ultra/case.html', 'ultratech', f'{H}/ultra/out', logo=f'{L}/ultratech.png', alt='UltraTech Cement logo', h=72)
assert sorted(os.listdir(f'{OUT}/ultratech/img')) == ['client-logo.webp', 'u_audio.webp', 'u_hero.webp', 'u_stages.webp'], os.listdir(f'{OUT}/ultratech/img')

# ---------- Ellenbarrie ----------
cp(f'{PROTO}/ellenbarrie.html', 'ellenbarrie/prototype.html')
case_page(f'{H}/ellen/case.html', 'ellenbarrie', f'{H}/ellen/out', logo=f'{L}/ellenbarrie.png', alt='Ellenbarrie Industrial Gases logo', h=76)

# ---------- ICA ----------
cp(f'{PROTO}/ica.html', 'ica/prototype.html')
case_page(f'{H}/ica/case.html', 'ica', f'{H}/ica/out', logo=f'{L}/ica.png', alt='ICA Italian Wood Finishes logo', h=96)

# ---------- Tata Power · Customer Smile ----------
cp(f'{PROTO}/tatapower.html', 'tatapower/prototype.html')
case_page(f'{H}/tata/case.html', 'tatapower', f'{H}/tata/out', logo=f'{L}/tata.png', alt='Tata Power logo', h=84)

# ---------- Casagrand ----------
cp(f'{PROTO}/casagrand.html', 'casagrand/prototype.html')
for f in os.listdir(f'{PROTO}/casagrand_proto'):
    cp(f'{PROTO}/casagrand_proto/{f}', f'casagrand/proto/{f}')
case_page(f'{H}/casa/case.html', 'casagrand', f'{H}/casa/out', logo=f'{L}/casagrand.png', alt='Casagrand logo', h=64)

# ---------- cache-busting: every local asset link gets ?v=<fingerprint> ----------
# Images/media are cached by browsers for a week; a changed file gets a new link, so visitors always see the latest.
import hashlib
_fp = {}
def fingerprint(path):
    if path not in _fp:
        h = hashlib.md5(open(path, 'rb').read())
        base, ext = os.path.splitext(path)
        if ext in ('.webp', '.avif'):                      # WebP/AVIF twins share one token (the cards swap .webp -> .avif in JS)
            twin = base + ('.avif' if ext == '.webp' else '.webp')
            if os.path.exists(twin):
                h = hashlib.md5(open(min(path, twin), 'rb').read() + open(max(path, twin), 'rb').read())
        _fp[path] = h.hexdigest()[:8]
    return _fp[path]
ASSET = re.compile(r'(["\'])((?:\.\./)?(?:images|media|assets|img|resume)/[^"\'?#\s]+)\1')
def bust_page(rel):
    path = f'{OUT}/{rel}'; base = os.path.dirname(path)
    def f(m):
        q, ref = m.group(1), m.group(2)
        target = os.path.normpath(os.path.join(base, ref))
        return f'{q}{ref}?v={fingerprint(target)}{q}' if os.path.isfile(target) else m.group(0)
    p = open(path).read()
    open(path, 'w').write(ASSET.sub(f, p))
for rel in ['index.html'] + [f'{d}/index.html' for d in ['amin', 'anchor', 'ultratech', 'ellenbarrie', 'ica', 'tatapower', 'casagrand']]:
    bust_page(rel)

# ---------- 404 page + Netlify caching ----------
open(f'{OUT}/404.html', 'w').write("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found · Parth Dake</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0}body{min-height:100vh;display:grid;place-items:center;padding:24px;background:#fff;color:#0A0A0A;font-family:Inter,system-ui,sans-serif;text-align:center}
img{width:56px;height:auto;margin:0 auto 28px;display:block}h1{font-size:clamp(34px,6vw,64px);font-weight:800;letter-spacing:-.04em;line-height:1}
p{margin:14px auto 28px;max-width:420px;color:#555;font-size:17px;line-height:1.6}
a.btn{display:inline-flex;align-items:center;gap:10px;height:52px;padding:0 22px;border-radius:12px;background:#0A0A0A;color:#fff;text-decoration:none;font-weight:600}
a.btn:hover{background:#222}
</style></head>
<body><main><img src="/images/logo.webp" alt="Parth Dake logo" width="160" height="150"><h1>Page not found</h1>
<p>This page doesn’t exist or has moved. Everything in the portfolio is one click away from the homepage.</p>
<a class="btn" href="/">Back to the portfolio</a></main></body></html>
""")
open(f'{OUT}/_headers', 'w').write("""# Netlify caching rules. Images, video and scripts are kept for a week; pages always load fresh.
/images/*
  Cache-Control: public, max-age=604800
/media/*
  Cache-Control: public, max-age=604800
/assets/*
  Cache-Control: public, max-age=604800
/amin/img/*
  Cache-Control: public, max-age=604800
/anchor/img/*
  Cache-Control: public, max-age=604800
/ultratech/img/*
  Cache-Control: public, max-age=604800
/ellenbarrie/img/*
  Cache-Control: public, max-age=604800
/ica/img/*
  Cache-Control: public, max-age=604800
/tatapower/img/*
  Cache-Control: public, max-age=604800
/casagrand/img/*
  Cache-Control: public, max-age=604800
/casagrand/proto/*
  Cache-Control: public, max-age=604800
""")

# ---------- minify HTML/CSS/JS of the pages (prototypes are left as built) ----------
MIN = os.environ.get('HTML_MINIFIER') or shutil.which('html-minifier-terser')
pages_to_min = ['index.html', '404.html'] + [f'{d}/index.html' for d in ['amin', 'anchor', 'ultratech', 'ellenbarrie', 'ica', 'tatapower', 'casagrand']]
if MIN:
    before = sum(os.path.getsize(f'{OUT}/{f}') for f in pages_to_min)
    for f in pages_to_min:
        subprocess.run([MIN, '--collapse-whitespace', '--conservative-collapse', '--remove-comments', '--minify-css', 'true',
                        '--minify-js', '{"compress":false,"mangle":false}', '--decode-entities', '-o', f'{OUT}/{f}', f'{OUT}/{f}'], check=True)
    after = sum(os.path.getsize(f'{OUT}/{f}') for f in pages_to_min)
    print(f'minified pages {before/1024:.0f} KB -> {after/1024:.0f} KB')
else:
    print('html-minifier-terser not found: pages left unminified (the site still works).')

# ---------- report ----------
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f'site total {tot/1e6:.1f} MB')
