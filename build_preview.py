"""Single-file preview of the hosted site: homepage + all case studies inlined.
Prototypes, the AMIN walkthrough video and the résumé PDF stay on the live site (too heavy to inline)."""
import base64, json, mimetypes, os, re

S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
MIME = {'.avif': 'image/avif', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webm': 'video/webm'}
def uri(path):
    return f'data:{MIME[os.path.splitext(path)[1]]};base64,' + base64.b64encode(open(path, 'rb').read()).decode()

def inline(html, base):
    def sub(m):
        q, ref = m.group(1), m.group(2)
        ref = ref.split('?')[0]
        p = os.path.normpath(os.path.join(base, ref))
        if os.path.splitext(ref)[1] in MIME and os.path.isfile(p) and 'walkthrough' not in ref:
            return q + uri(p) + q
        return m.group(0)
    return re.sub(r'(["\'])((?:\.\./)?(?:images|media|img)/[^"\']+)\1', sub, html)

PROTO = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;font-family:Inter,system-ui,sans-serif;background:#f6f6f6;color:#0a0a0a;text-align:center;padding:24px;box-sizing:border-box}
h1{font-size:28px;margin:0 0 10px;letter-spacing:-.02em}p{color:#555;max-width:440px;line-height:1.6;margin:0 auto}</style></head>
<body><div><h1>Interactive prototype</h1><p>The full prototype is too heavy for this single-file preview. It opens from this button on the live site.</p></div></body></html>"""

home = open(f'{S}/index.html').read()
pages = {
    'case': 'amin', 'anchorCase': 'anchor', 'ultraCase': 'ultratech', 'ellenCase': 'ellenbarrie', 'icaCase': 'ica', 'tataCase': 'tatapower', 'casaCase': 'casagrand',
}
P = {}
for key, folder in pages.items():
    P[key] = inline(open(f'{S}/{folder}/index.html').read(), f'{S}/{folder}')
for key in ['proto', 'anchorProto', 'ellenProto', 'icaProto', 'tataProto', 'casaProto']:
    P[key] = PROTO

home = inline(home, S)
blob = json.dumps(P).replace('</', '<\\/')
old = re.search(r'window\.__PAGES\s*=\s*\{[^;<]*\}', home).group(0)
home = home.replace(old, 'window.__PAGES = ' + blob, 1)
home, n = re.subn(r'f\.src\s*=\s*P\[key\]', 'f.srcdoc=P[key]', home)
assert n == 1, n
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'portfolio-preview.html'), 'w').write(home)
print(f'{len(home)/1e6:.1f} MB')
