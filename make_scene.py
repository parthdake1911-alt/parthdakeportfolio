"""Prepare the hero (daylight doorway) and the footer (studio) images from Parth's generated pictures.
Enlarged with Lanczos + a light sharpen, exported as WebP at sizes that stay crisp on retina screens."""
import os, numpy as np
from PIL import Image, ImageFilter
H = os.path.dirname(os.path.abspath(__file__)); OUT = f'{H}/scene'
def export(src, out, w, q=82, sharpen=True):
    im = Image.open(src).convert('RGB')
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if sharpen: im = im.filter(ImageFilter.UnsharpMask(1.1, 35, 2))
    im.save(out, 'WEBP', quality=q, method=6)
    print(os.path.basename(out), im.size, os.path.getsize(out) // 1024, 'KB')
# hero: the same daylight picture serves phones (framed in code to keep the figure and the door)
export(f'{H}/scene/src/day-desktop.png', f'{OUT}/door-d.webp', 2560)
export(f'{H}/scene/src/day-desktop.png', f'{OUT}/door-m.webp', 1800)
# footer: the studio — sketching, thinking, building
export(f'{H}/scene/src/studio.png', f'{OUT}/studio-d.webp', 2304, q=84)
export(f'{H}/scene/src/studio.png', f'{OUT}/studio-m.webp', 1280, q=84)

# ---- The world beyond the door: small crops of Parth's real screens, shown floating inside the doorway
from PIL import Image as _I
P = f'{OUT}/portal'; os.makedirs(P, exist_ok=True)
for k, src, kind in [('tata', 'tata/out/t_home.webp', 'phone'), ('ultra', 'ultra/out/u_hero.webp', 'phone'),
                     ('casa', 'casa/out/c_hero.webp', 'web'), ('ica', 'ica/out/i_trend.webp', 'web'),
                     ('anchor', 'anchor/out/a_dash.webp', 'web'), ('amin', 'amin/out/a_globe.webp', 'web')]:
    im = _I.open(f'{H}/{src}').convert('RGB')
    if kind == 'web':
        w, h = im.width, round(im.width * 10 / 16); im = im.crop((0, 0, w, min(h, im.height))).resize((360, 225), _I.LANCZOS)
    else:
        w, h = im.width, round(im.width * 19 / 9); im = im.crop((0, 0, w, min(h, im.height))).resize((180, 380), _I.LANCZOS)
    im.save(f'{P}/{k}.webp', 'WEBP', quality=84, method=6)
print('portal screens:', sorted(os.listdir(P)))
