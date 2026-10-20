"""Prepare the Doorway hero images from Parth's two generated pictures.
Upscaled 2x (EDSR) when available, gently graded so the night reads as warm dusk rather than black,
and exported as WebP plus a soft, blurred copy used behind the project cards."""
import os, numpy as np
from PIL import Image, ImageFilter
H = os.path.dirname(os.path.abspath(__file__)); OUT = f'{H}/scene'
SR = '/tmp/claude-0/-home-claude/056a394b-02b8-5f93-a710-c26895cbb183/scratchpad/sr'
SRC = {'d': f'{H}/scene/src/door-desktop.png', 'm': f'{H}/scene/src/door-mobile.png'}
def grade(im):
    a = np.asarray(im).astype(np.float32) / 255
    lift = np.array([.040, .028, .034])                # lift the blacks toward a warm plum, not grey
    a = a + lift * (1 - a) ** 3
    a = np.clip(a * 1.04, 0, 1)                        # a touch more exposure
    return Image.fromarray((a * 255 + .5).astype(np.uint8))
for k, src in SRC.items():
    up = f'{SR}/door_{k}.png'
    im = Image.open(up).convert('RGB') if os.path.exists(up) else Image.open(src).convert('RGB').resize(
        (Image.open(src).width * 2, Image.open(src).height * 2), Image.LANCZOS)
    im = grade(im)
    w = 2560 if k == 'd' else 1440
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 40, 2))
    im.save(f'{OUT}/door-{k}.webp', 'WEBP', quality=80, method=6)
    sw = 640 if k == 'd' else 400
    s = im.resize((sw, round(im.height * sw / im.width)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(sw / 60))
    s.save(f'{OUT}/door-{k}-soft.webp', 'WEBP', quality=70, method=6)
    print(k, im.size, os.path.getsize(f'{OUT}/door-{k}.webp') // 1024, 'KB', 'upscaled' if os.path.exists(up) else 'lanczos')

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
