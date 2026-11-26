"""Rebuild only the homepage (site/index.html) from template.html, using the assets already in site/.
Use this for homepage-only changes when the full build_all.py toolchain (optimized/ media) isn't available."""
import os, re, json, hashlib, shutil, subprocess
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, 'site')

covers = {k: f'images/cards/{k}.webp' for k in ['allin', 'padaav', 'amin', 'tata', 'ica', 'anchor', 'casagrand']}
DECK = {}
for k in ['tata', 'casagrand', 'ica', 'anchor', 'amin']:
    logo = f'images/deck/logo-{k}.svg' if os.path.exists(f'{OUT}/images/deck/logo-{k}.svg') else f'images/deck/logo-{k}.webp'
    DECK[k] = {'img': f'images/deck/{k}.webp', 'logo': logo}
for k in ['allin', 'padaav']:
    DECK[k] = {'img': f'images/deck/{k}.webp', 'logo': f'images/deck/{k}.webp'}
pages = {'case': 'amin/', 'proto': 'amin/prototype.html', 'anchorCase': 'anchor/', 'anchorProto': 'anchor/prototype.html',
         'icaCase': 'ica/', 'icaProto': 'ica/prototype.html', 'tataCase': 'tatapower/', 'tataProto': 'tatapower/prototype.html',
         'casaCase': 'casagrand/', 'casaProto': 'casagrand/prototype.html', 'allinCase': 'allin/', 'padaavCase': 'padaav/', 'padaavProto': 'padaav/prototype.html'}
rep = {
    '{{STUDIO_D}}': 'images/studio-d.webp', '{{STUDIO_M}}': 'images/studio-m.webp',
    '{{DOOR_D}}': 'images/door-d.webp', '{{DOOR_M}}': 'images/door-m.webp',
    '{{IMAGES}}': json.dumps(covers), '{{DECK}}': json.dumps(DECK),
    '{{HL_TATA}}': 'images/hl-tata.webp', '{{HL_ICA}}': 'images/hl-ica.webp', '{{HL_CASA}}': 'images/hl-casa.webp',
    '{{CONVOFULL_AVIF}}': 'images/convo_full.avif', '{{CONVOFULL}}': 'images/convo_full.webp',
    '{{CONVO_AVIF}}': 'images/convo_crop.avif', '{{CONVO}}': 'images/convo_crop.webp',
    '{{BCW_AVIF}}': 'images/bcw.avif', '{{BCW}}': 'images/bcw.webp',
    '{{LOGO}}': 'images/logo.webp', '{{PAGES}}': json.dumps(pages),
}
t = open(f'{H}/template.html').read()
for k, v in rep.items():
    t = t.replace(k, v)
for a, b in [('amin', 'amin'), ('anchor', 'anchor'), ('ica', 'ica'), ('tata', 'tatapower'), ('casagrand', 'casagrand'), ('allin', 'allin'), ('padaav', 'padaav')]:
    t = t.replace(f"href: '{a}-case-study.html'", f"href: '{b}/'")
assert "f.srcdoc = P[key];" in t
t = t.replace("f.srcdoc = P[key];", "f.src = P[key];")
assert '{{' not in re.sub(r'<script>window.__PAGES.*?</script>', '', t), 'unfilled placeholder'

ASSET = re.compile(r'(["\'])((?:\.\./)?(?:images|media|assets|img|resume)/[^"\'?#\s]+)\1')
def fp(path):
    h = hashlib.md5(open(path, 'rb').read()); base, ext = os.path.splitext(path)
    if ext in ('.webp', '.avif'):
        twin = base + ('.avif' if ext == '.webp' else '.webp')
        if os.path.exists(twin):
            h = hashlib.md5(open(min(path, twin), 'rb').read() + open(max(path, twin), 'rb').read())
    return h.hexdigest()[:8]
t = ASSET.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={fp(os.path.join(OUT, m.group(2)))}{m.group(1)}' if os.path.isfile(os.path.join(OUT, m.group(2))) else m.group(0), t)
open(f'{OUT}/index.html', 'w').write(t)

MIN = os.environ.get('HTML_MINIFIER') or shutil.which('html-minifier-terser')
if MIN:
    subprocess.run([MIN, '--collapse-whitespace', '--conservative-collapse', '--remove-comments', '--minify-css', 'true',
                    '--minify-js', '{"compress":false,"mangle":false}', '--decode-entities', '-o', f'{OUT}/index.html', f'{OUT}/index.html'], check=True)
print('built site/index.html', os.path.getsize(f'{OUT}/index.html') // 1024, 'KB')
