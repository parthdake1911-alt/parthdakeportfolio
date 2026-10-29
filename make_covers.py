"""Minimal project-card covers: brand logo + a real screen from the project, on a light brand tint.

Writes cards/<key>.webp (720 x 814, the card frame). The previous covers are kept in cards/_previous/.
Run before optimize_media.py (build_all.py does this).
"""
import asyncio, os, shutil
from pathlib import Path
from playwright.async_api import async_playwright

H = Path(__file__).resolve().parent
W, HT = 720, 814

#  key: (background tint, logo file, logo height, shot file, kind, shot position)
COVERS = {
    'amin':        ('#F1EEFB', 'logos/amin.png',        40, 'amin/out/a_globe.webp',  'browser', 'top'),
    'anchor':      ('#EEF2F9', 'logos/anchor.svg',      52, 'anchor/out/a_dash.webp', 'browser', 'top left'),
    'ellenbarrie': ('#F8EEEE', 'logos/ellenbarrie.png', 66, 'ellen/out/r_hero.webp',  'browser', 'top'),
    'ica':         ('#F2EFEA', 'logos/ica.png',         82, 'ica/out/i_trend.webp',   'browser', 'top'),
    'tata':        ('#EAF1FB', 'logos/tata.png',        66, 'tata/out/t_home.webp',   'phone',   'top'),
    'casagrand':   ('#FBF3E3', 'logos/casagrand.png',   48, 'casa/out/c_hero.webp',   'browser', 'top'),
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%dpx;height:%dpx;overflow:hidden}
body{background:var(--bg);position:relative;font-family:Inter,system-ui,sans-serif}
.logo{position:absolute;left:52px;top:50px;height:var(--lh);max-width:300px;object-fit:contain;object-position:left center}
.browser{position:absolute;left:52px;top:178px;width:760px;border-radius:16px 0 0 0;overflow:hidden;background:#fff;
         box-shadow:0 2px 0 rgba(0,0,0,.03),0 30px 60px -10px rgba(20,20,40,.22)}
.browser .bar{height:30px;background:#fff;border-bottom:1px solid #ececec;display:flex;align-items:center;gap:7px;padding-left:16px}
.browser .bar i{width:9px;height:9px;border-radius:50%%;background:#dcdcdc}
.browser img{display:block;width:100%%;height:520px;object-fit:cover;object-position:var(--pos)}
.phone{position:absolute;left:50%%;transform:translateX(-50%%);top:170px;width:330px;border-radius:44px;background:#0b0b0b;padding:10px 10px 0;
       box-shadow:0 30px 60px -10px rgba(20,20,40,.30)}
.phone img{display:block;width:100%%;height:700px;object-fit:cover;object-position:var(--pos);border-radius:34px 34px 0 0}
.center{position:absolute;inset:0;display:grid;place-items:center}
.center img{height:var(--lh);max-width:520px;object-fit:contain}
""" % (W, HT)

def page(key):
    bg, logo, lh, shot, kind, pos = COVERS[key]
    logo_uri = (H / logo).as_uri()
    if kind == 'logo':
        body = f'<div class="center"><img src="{logo_uri}" alt=""></div>'
    else:
        shot_uri = (H / shot).as_uri()
        frame = (f'<div class="browser"><div class="bar"><i></i><i></i><i></i></div><img src="{shot_uri}" alt=""></div>'
                 if kind == 'browser' else f'<div class="phone"><img src="{shot_uri}" alt=""></div>')
        body = f'<img class="logo" src="{logo_uri}" alt="">{frame}'
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body style="--bg:{bg};--lh:{lh}px;--pos:{pos or "center"}">{body}</body></html>')

async def main():
    prev = H / 'cards' / '_previous'
    prev.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': W, 'height': HT}, device_scale_factor=1)
        for key in COVERS:
            out = H / 'cards' / f'{key}.webp'
            if out.exists() and not (prev / out.name).exists():
                shutil.copy(out, prev / out.name)          # keep the original cover once
            tmp = H / f'_cover_{key}.html'
            tmp.write_text(page(key))
            await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(300)
            png = H / f'_cover_{key}.png'
            await pg.screenshot(path=str(png))
            from PIL import Image
            Image.open(png).convert('RGB').save(out, 'WEBP', quality=86, method=6)
            tmp.unlink(); png.unlink()
            print('cover', key, out.stat().st_size // 1024, 'KB')
        await b.close()

asyncio.run(main())
