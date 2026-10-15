"""Rebuild everything, in order:
  1. each case-study page (case folders: body.html + extra.css -> case.html)
  2. project-card covers (make_covers.py), lighter images, poster, résumé (optimize_media.py) and prototypes (optimize_prototypes.py)
  3. the Netlify site folder ./site (build_site.py)
  4. a single-file offline preview ./portfolio-preview.html (build_preview.py)
Run:  python3 build_all.py
"""
import os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
def run(script, cwd=H):
    print('>>', os.path.relpath(os.path.join(cwd, script), H))
    subprocess.run([sys.executable, script], cwd=cwd, check=True)
for d in ['anchor', 'ultra', 'ellen', 'ica', 'tata']:
    run('build.py', os.path.join(H, d))
run('make_covers.py')
run('optimize_media.py')
run('optimize_prototypes.py')
run('build_site.py')
run('build_preview.py')
print('done: upload the "site" folder to Netlify')
