"""Assemble the two deliverables:
  dist/Parth-Portfolio-Netlify-Upload.zip   README.txt + "Netlify Upload" folder (the built site)
  dist/Parth-Portfolio-Source-Project.zip   everything needed to edit and rebuild the site
"""
import glob, os, re, shutil, zipfile

H = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(H, 'dist')
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)

def zipdir(folder, zpath, arc_root):
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _, files in os.walk(folder):
            for f in sorted(files):
                full = os.path.join(root, f)
                z.write(full, os.path.join(arc_root, os.path.relpath(full, folder)))

# ---------- 1. Netlify upload ----------
# index.html sits at the very top of the ZIP, so the unzipped folder is exactly what Netlify needs
zipdir(os.path.join(H, 'site'), os.path.join(DIST, 'Parth-Portfolio-Netlify-Upload.zip'), '')
shutil.copy(os.path.join(H, 'README.txt'), os.path.join(DIST, 'README.txt'))

# ---------- 2. Source project ----------
SRC = os.path.join(DIST, 'source', 'Parth-Portfolio-Source')
def take(rel):
    for p in glob.glob(os.path.join(H, rel)):
        dst = os.path.join(SRC, os.path.relpath(p, H))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        (shutil.copytree if os.path.isdir(p) else shutil.copy)(p, dst)

for f in ['build_all.py', 'build_site.py', 'build_preview.py', 'optimize_media.py', 'optimize_prototypes.py', 'make_packages.py',
          'template.html', 'intro.mp4', 'intro.webm', 'README.txt', 'cards', 'logos', 'resume', 'vendor']:
    take(f)
shutil.copy(os.path.join(H, 'README-SOURCE.txt'), os.path.join(SRC, 'README-SOURCE.txt'))

# case folders: page sources, the images they actually reference, and the original prototypes
def placeholders(*files):
    keys = set()
    for f in files:
        if os.path.exists(f):
            keys |= set(re.findall(r'\{\{([A-Za-z0-9_]+)\}\}', open(f).read()))
    return keys
cases = {
    'amin':   (['case.html', 'build_case.py', 'src/portal.html', 'out/poster.jpg', 'out/amin-walkthrough.mp4', 'out/logo.png'], ['case.html']),
    'anchor': (['base_style.css', 'base_script.js', 'body.html', 'extra.css', 'build.py', 'case.html', 'src/anchor.html'], ['body.html']),
    'ultra':  (['body.html', 'extra.css', 'build.py', 'case.html'], ['body.html']),
    'ellen':  (['body.html', 'extra.css', 'build.py', 'case.html', 'src/redesign.html', 'src/original.png'], ['body.html']),
    'ica':    (['body.html', 'extra.css', 'build.py', 'case.html', 'src/ica.html'], ['body.html']),
    'tata':   (['body.html', 'extra.css', 'build.py', 'case.html', 'src/mcs.html'], ['body.html']),
}
for d, (files, tpl) in cases.items():
    for f in files:
        take(f'{d}/{f}')
    for k in placeholders(*[os.path.join(H, d, t) for t in tpl]):
        if k not in ('LOGO', 'POSTER', 'VIDEOSRC'):
            take(f'{d}/out/{k}.webp')
zipdir(os.path.join(DIST, 'source'), os.path.join(DIST, 'Parth-Portfolio-Source-Project.zip'), '')

for z in sorted(glob.glob(os.path.join(DIST, '*.zip'))):
    print(f'{os.path.basename(z):42s} {os.path.getsize(z)/1e6:5.1f} MB')
