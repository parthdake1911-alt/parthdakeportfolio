"""Make the lighter homepage images, video poster, résumé and local jQuery used by build_site.py.

Inputs (never modified): cards/, intro.mp4, resume/Parth-Dake-Resume-original.pdf, vendor/jquery-3.7.1.min.js
Outputs: optimized/images/, optimized/media/, optimized/resume/, optimized/jquery-3.7.1.min.js
"""
import io, os, re, shutil, subprocess
from PIL import Image

H = os.path.dirname(os.path.abspath(__file__))
OPT = os.path.join(H, 'optimized')
for d in ['images/cards', 'media', 'resume']:
    os.makedirs(os.path.join(OPT, d), exist_ok=True)

def avif(im, path, q=60):
    im.save(path, 'AVIF', quality=q, speed=4)

# Project covers: AVIF (with the existing WebP as fallback). All cards share the 720x814 frame.
for k in ['amin', 'ultratech', 'tata', 'ica', 'ellenbarrie', 'anchor', 'sp']:
    im = Image.open(f'{H}/cards/{k}.webp').convert('RGB')
    fh = round(im.width * 814 / 720)
    if im.height > fh + 4:                       # taller than the frame: keep only the visible part
        y = round((im.height - fh) * (0.88 if k == 'anchor' else 0.5))
        im = im.crop((0, y, im.width, y + fh))
        im.save(f'{OPT}/images/cards/{k}.webp', 'WEBP', quality=82, method=6)
    avif(im, f'{OPT}/images/cards/{k}.avif')

# About section photos
for k in ['convo_crop', 'convo_full', 'bcw']:
    im = Image.open(f'{H}/cards/{k}.webp')
    avif(im.convert('RGBA' if im.mode == 'RGBA' else 'RGB'), f'{OPT}/images/{k}.avif')

# Poster frame for the hero video, so something shows instantly
png = f'{OPT}/media/_poster.png'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{H}/intro.mp4', '-frames:v', '1', '-vf', 'scale=720:-2', png], check=True)
Image.open(png).convert('RGB').save(f'{OPT}/media/intro-poster.webp', 'WEBP', quality=72, method=6)
os.remove(png)

# Résumé: the PDF is outlined vector text with 6-decimal coordinates; 2 decimals (1/100 pt) looks identical
import pikepdf
num = re.compile(rb'(-?\d+\.\d{3,})')
def rnd(m):
    s = (b'%.2f' % round(float(m.group(1)), 2)).rstrip(b'0').rstrip(b'.')
    return b'0' if s in (b'-0', b'') else s
pdf = pikepdf.open(f'{H}/resume/Parth-Dake-Resume-original.pdf')
for page in pdf.pages:
    cs = page.obj.Contents
    for c in (cs if isinstance(cs, pikepdf.Array) else [cs]):
        lines = c.read_bytes().split(b'\n')
        c.write(b'\n'.join(l if (b'(' in l or b'<' in l) else num.sub(rnd, l) for l in lines))
pdf.remove_unreferenced_resources()
pdf.save(f'{OPT}/resume/Parth-Dake-Resume.pdf', compress_streams=True,
         object_stream_mode=pikepdf.ObjectStreamMode.generate, recompress_flate=True)

shutil.copy(f'{H}/vendor/jquery-3.7.1.min.js', f'{OPT}/jquery-3.7.1.min.js')
print('media optimized')
