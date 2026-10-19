"""Portrait (3:4) full-bleed images for the scroll deck of project cards: cards/deck/<id>.webp, 720 x 960.
Each comes from a real screen in the case study; (crop centre x, crop centre y) picks the part that reads best."""
from pathlib import Path
from PIL import Image, ImageDraw
H = Path(__file__).resolve().parent
OUT = H / 'cards' / 'deck'; OUT.mkdir(parents=True, exist_ok=True)
W, HT = 720, 960
SRC = {
    'tata':        ('tata/out/t_home.webp',  .5, 0.0),
    'casagrand':   ('casa/out/c_hero.webp',  .5, .5),
    'ica':         ('ica/out/i_trend.webp',  .62, .5),
    'anchor':      ('anchor/out/a_dash.webp', .2, .0),
    'amin':        ('amin/out/a_globe.webp', .8, .5),
    'ellenbarrie': ('ellen/out/r_hero.webp', .86, .5),
    'ultratech':   ('ultra/out/u_hero.webp', .5, 0.0),
}
def crop(im, fx, fy):
    r = W / HT
    if im.width / im.height > r:
        cw, ch = round(im.height * r), im.height
    else:
        cw, ch = im.width, round(im.width / r)
    x = min(max(0, round(im.width * fx - cw / 2)), im.width - cw)
    y = min(max(0, round((im.height - ch) * fy)), im.height - ch)
    return im.crop((x, y, x + cw, y + ch)).resize((W, HT), Image.LANCZOS)
for k, (f, fx, fy) in SRC.items():
    crop(Image.open(H / f).convert('RGB'), fx, fy).save(OUT / f'{k}.webp', 'WEBP', quality=82, method=6)
# Shapoorji Pallonji: work in progress, no screens yet -> brand tint with the logo
bg = Image.new('RGB', (W, HT), '#EDF3F9')
lg = Image.open(H / 'logos/sp.png').convert('RGBA'); s = 440 / lg.width
lg = lg.resize((440, round(lg.height * s)), Image.LANCZOS)
bg.paste(lg, ((W - lg.width) // 2, (HT - lg.height) // 2 - 20), lg)
bg.save(OUT / 'sp.webp', 'WEBP', quality=86, method=6)
print('deck images:', sorted(p.name for p in OUT.iterdir()))
