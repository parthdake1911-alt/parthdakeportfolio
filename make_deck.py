"""Portrait (3:4) project cards for the scroll deck: cards/deck/<id>.webp, 720 x 960 (rendered at 2x for sharpness, saved at 720).
A soft brand-tinted card with the client's logo large at the top and a real screen from the project rising from the bottom.
Text (type, name, button) is laid over in HTML, so the image itself carries no text of ours."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
H = Path(__file__).resolve().parent
OUT = H / 'cards' / 'deck'; OUT.mkdir(parents=True, exist_ok=True)
W, HT = 720, 960
#  id: (tint top, tint bottom, logo, logo height, shot, kind, object-position)
D = {
    'tata':        ('#F3F7FD', '#D9E6F8', 'logos/tata.png',        150, 'tata/out/t_home.webp',  'phone',   'top'),
    'casagrand':   ('#FDF9F1', '#F3E4C6', 'logos/casagrand.png',   104, 'casa/out/c_hero.webp',  'browser', 'top'),
    'ica':         ('#F8F6F2', '#E6DFD3', 'logos/ica.png',         170, 'ica/out/i_trend.webp',  'browser', 'top'),
    'anchor':      ('#F5F7FB', '#DCE3F0', 'logos/anchor.svg',      104, 'anchor/out/a_dash.webp', 'browser', 'top left'),
    'amin':        ('#F7F5FD', '#E2DCF6', 'logos/amin.png',         88, 'amin/out/a_globe.webp', 'browser', 'top left'),
    'ellenbarrie': ('#FBF5F5', '#F0DADA', 'logos/ellenbarrie.png', 130, 'ellen/out/r_hero.webp', 'browser', 'top left'),
    'ultratech':   ('#FDFBF1', '#F2EAC4', 'logos/ultratech.png',   140, 'ultra/out/u_hero.webp', 'phone',   'top'),
    'sp':          ('#F4F8FC', '#DCE7F2', 'logos/sp.png',          190, None,                    'none',    None),
}
CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{HT}px;overflow:hidden}}
body{{position:relative;background:linear-gradient(170deg,var(--a) 0%,var(--a) 30%,var(--b) 100%)}}
body::before{{content:"";position:absolute;inset:0;background:radial-gradient(ellipse 70% 40% at 50% 12%,rgba(255,255,255,.9),rgba(255,255,255,0) 70%)}}
.logo{{position:absolute;left:50%;top:var(--lt);transform:translate(-50%,-50%);height:var(--lh);max-width:470px;object-fit:contain}}
.browser{{position:absolute;left:60px;right:60px;top:372px;height:700px;border-radius:22px 22px 0 0;overflow:hidden;background:#fff;
  box-shadow:0 2px 0 rgba(255,255,255,.6) inset,0 40px 80px -20px rgba(20,25,45,.35),0 0 0 1px rgba(20,25,45,.06)}}
.browser .bar{{height:34px;background:#fff;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px;padding-left:18px}}
.browser .bar i{{width:10px;height:10px;border-radius:50%;background:#e2e2e2}}
.browser img{{display:block;width:100%;height:calc(100% - 34px);object-fit:cover;object-position:var(--pos)}}
.phone{{position:absolute;left:50%;transform:translateX(-50%);top:330px;width:330px;height:720px;border-radius:52px;background:#0b0b0b;padding:11px;
  box-shadow:0 50px 90px -24px rgba(20,25,45,.45)}}
.phone img{{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:42px}}
"""
def page(k):
    a, b, logo, lh, shot, kind, pos = D[k]
    lt = 190 if kind != 'none' else 420
    body = f'<img class="logo" src="{(H / logo).as_uri()}" style="--lh:{lh}px;--lt:{lt}px">'
    if kind == 'browser':
        body += f'<div class="browser"><div class="bar"><i></i><i></i><i></i></div><img src="{(H / shot).as_uri()}" style="--pos:{pos}"></div>'
    elif kind == 'phone':
        body += f'<div class="phone"><img src="{(H / shot).as_uri()}"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="--a:{a};--b:{b}">{body}</body></html>'
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch()
        pg = await br.new_page(viewport={'width': W, 'height': HT}, device_scale_factor=2)
        for k in D:
            tmp = H / f'_deck_{k}.html'; tmp.write_text(page(k))
            await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(250)
            png = H / f'_deck_{k}.png'; await pg.screenshot(path=str(png))
            Image.open(png).convert('RGB').resize((W, HT), Image.LANCZOS).save(OUT / f'{k}.webp', 'WEBP', quality=86, method=6)
            tmp.unlink(); png.unlink()
        await br.close()
    print('deck cards:', sorted(x.name for x in OUT.iterdir()))
asyncio.run(main())
