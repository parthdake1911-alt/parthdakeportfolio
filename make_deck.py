"""Portrait (3:4) project cards for the scroll deck: cards/deck/<id>.webp, 720 x 960 (rendered at 2x for sharpness, saved at 720).
A dark night card with the client's logo large at the top and a real screen from the project rising from the bottom.
Text (type, name, button) is laid over in HTML, so the image itself carries no text of ours."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
H = Path(__file__).resolve().parent
OUT = H / 'cards' / 'deck'; OUT.mkdir(parents=True, exist_ok=True)
W, HT = 720, 960
#  id: (brand glow colour, logo, logo height, shot, kind, object-position)
D = {
    'tata':        ('#2F7BFF', 'logos/tata.png',        104, 'tata/out/t_home.webp',  'phone',   'top'),
    'casagrand':   ('#FFB536', 'logos/casagrand.png',    66, 'casa/out/c_hero.webp',  'browser', 'top'),
    'ica':         ('#E2483B', 'logos/ica.png',         112, 'ica/out/i_trend.webp',  'browser', 'top'),
    'anchor':      ('#4C6FFF', 'logos/anchor.svg',       66, 'anchor/out/a_dash.webp', 'browser', 'top left'),
    'amin':        ('#8B5CF6', 'logos/amin.png',         58, 'amin/out/a_globe.webp', 'browser', 'top left'),
    'ultratech':   ('#FFD400', 'logos/ultratech.png',    92, 'ultra/out/u_hero.webp', 'phone',   'top'),
    'sp':          ('#2E7DD6', 'logos/sp.png',          120, None,                    'none',    None),
}
# Night cards: each project is a lit doorway. Dark glass, the client's colour glowing from within,
# the logo on a frosted plate (so every brand colour reads true on dark), and the real screen rising into the light.
CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{HT}px;overflow:hidden}}
body{{position:relative;background:linear-gradient(172deg,#17110f 0%,#0d0a0b 55%,#0a0809 100%)}}
.glow{{position:absolute;inset:0;background:radial-gradient(60% 38% at 50% 26%,color-mix(in srgb,var(--c) 42%,transparent),transparent 72%),
  radial-gradient(70% 30% at 50% 104%,rgba(255,170,100,.30),transparent 70%)}}
.grid{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.16) 1px,transparent 1.4px);background-size:22px 22px;
  -webkit-mask-image:radial-gradient(65% 45% at 50% 30%,#000,transparent 75%);opacity:.55}}
.plate{{position:absolute;left:50%;top:var(--lt);transform:translate(-50%,-50%);padding:26px 40px;border-radius:30px;
  background:linear-gradient(160deg,rgba(255,255,255,.97),rgba(255,255,255,.86));box-shadow:0 0 0 1px rgba(255,255,255,.6) inset,0 20px 50px rgba(0,0,0,.45),0 0 70px color-mix(in srgb,var(--c) 35%,transparent)}}
.plate img{{display:block;height:var(--lh);max-width:430px;object-fit:contain}}
.browser{{position:absolute;left:56px;right:56px;top:392px;height:700px;border-radius:22px 22px 0 0;overflow:hidden;background:#111;
  box-shadow:0 0 0 1px rgba(255,255,255,.14),0 -10px 90px color-mix(in srgb,var(--c) 30%,transparent),0 40px 80px -20px rgba(0,0,0,.6)}}
.browser .bar{{height:34px;background:#1b1517;border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;gap:8px;padding-left:18px}}
.browser .bar i{{width:10px;height:10px;border-radius:50%;background:rgba(255,255,255,.18)}}
.browser img{{display:block;width:100%;height:calc(100% - 34px);object-fit:cover;object-position:var(--pos)}}
.phone{{position:absolute;left:50%;transform:translateX(-50%);top:350px;width:330px;height:720px;border-radius:52px;background:#050505;padding:11px;
  box-shadow:0 0 0 1px rgba(255,255,255,.18),0 0 0 3px #1c1c1c,0 -10px 90px color-mix(in srgb,var(--c) 32%,transparent),0 50px 90px -24px rgba(0,0,0,.7)}}
.phone img{{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:42px}}
"""
def page(k):
    c, logo, lh, shot, kind, pos = D[k]
    lt = 200 if kind != 'none' else 430
    body = f'<div class="glow"></div><div class="grid"></div><div class="plate" style="--lt:{lt}px"><img src="{(H / logo).as_uri()}" style="--lh:{lh}px"></div>'
    if kind == 'browser':
        body += f'<div class="browser"><div class="bar"><i></i><i></i><i></i></div><img src="{(H / shot).as_uri()}" style="--pos:{pos}"></div>'
    elif kind == 'phone':
        body += f'<div class="phone"><img src="{(H / shot).as_uri()}"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="--c:{c}">{body}</body></html>'
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
