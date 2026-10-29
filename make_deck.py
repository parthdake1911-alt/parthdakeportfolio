"""Portrait (3:4) project cards for the scroll deck: cards/deck/<id>.webp, 720 x 960 (rendered at 2x for sharpness, saved at 720).
A poster card with the client's logo large at the top and a real screen from the project rising from the bottom.
Text (type, name, button) is laid over in HTML, so the image itself carries no text of ours."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np
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
}
# Poster cards: the work fills the card edge to edge, like a film poster or an App Store story.
# A dark fade top and bottom gives the logo (small, on a frosted chip) and the edge light room to breathe.
# Phone projects sit on an atmosphere made from their own screen, blurred, so every card carries its brand's colour.
CSS = f"""*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{HT}px;overflow:hidden;background:#F6F2EB}}
.full{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:var(--pos)}}
.atmo{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.brand{{position:absolute;inset:0}}
.win{{position:absolute;left:70px;top:250px;width:1040px;height:700px;border-radius:18px;overflow:hidden;background:#111;
  transform:perspective(1700px) rotateY(-24deg) rotateX(9deg) rotateZ(1.5deg);transform-origin:left center;
  box-shadow:0 0 0 1px rgba(23,18,15,.08),0 40px 60px -20px rgba(70,45,30,.35)}}
.win .bar{{height:36px;background:#fff;display:flex;align-items:center;gap:9px;padding-left:20px}}
.win .bar i{{width:11px;height:11px;border-radius:50%;background:rgba(23,18,15,.14)}}
.win img{{display:block;width:100%;height:calc(100% - 36px);object-fit:cover;object-position:var(--pos)}}
.win::after{{content:"";position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.22),transparent 35%)}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(246,242,235,.55) 0%,rgba(246,242,235,0) 24%,rgba(246,242,235,0) 70%,rgba(246,242,235,.65) 100%)}}
.edge{{position:absolute;inset:0;background:radial-gradient(60% 40% at 100% 0%,rgba(255,196,140,.35),transparent 70%)}}
.chip{{position:absolute;left:40px;top:40px;padding:16px 22px;border-radius:20px;background:rgba(255,255,255,.96);box-shadow:0 0 0 1px rgba(23,18,15,.06),0 10px 30px rgba(70,45,30,.16)}}
.chip img{{display:block;height:var(--lh);max-width:300px;object-fit:contain}}
.center{{left:50%;top:50%;transform:translate(-50%,-50%);padding:30px 44px;border-radius:30px}}
.phone{{position:absolute;left:50%;transform:translateX(-50%);top:190px;width:380px;height:830px;border-radius:58px;background:#050505;padding:12px;
  box-shadow:0 0 0 1px rgba(255,255,255,.2),0 0 0 3px #1a1a1a,0 40px 60px -10px rgba(70,45,30,.4)}}
.phone img{{display:block;width:100%;height:100%;object-fit:cover;object-position:top;border-radius:47px}}
"""
D = {
    #  id: (brand colour, logo, logo height on chip, shot, kind, object-position)
    'tata':      ('#2F7BFF', 'logos/tata.png',      54, 'tata/out/t_home.webp',   'phone',   'top'),
    'casagrand': ('#FFB536', 'logos/casagrand.png', 34, 'casa/out/c_hero.webp',   'tilt',    'top'),
    'ica':       ('#E2483B', 'logos/ica.png',       58, 'ica/out/i_trend.webp',   'tilt',    'top'),
    'anchor':    ('#4C6FFF', 'logos/anchor.svg',    34, 'anchor/out/a_dash.webp', 'tilt',    'left top'),
    'amin':      ('#8B5CF6', 'logos/amin.png',      32, 'amin/out/a_globe.webp',  'tilt',    'top left'),
}
from PIL import ImageFilter, ImageEnhance
def atmo(k, shot):
    """The soft colour field behind the work: the project's own screen, cover-fit, heavily blurred in 16-bit-ish float, then dimmed."""
    out = H / f'_atmo_{k}.png'
    im = Image.open(H / shot).convert('RGB')
    w, h = 1440, 1920; sc = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    l, t = (im.width - w) // 2, 0; im = im.crop((l, t, l + w, t + h))
    im = im.resize((360, 480), Image.LANCZOS).filter(ImageFilter.GaussianBlur(28)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    im = ImageEnhance.Color(im).enhance(.9); im = ImageEnhance.Brightness(im).enhance(1.08)
    im = Image.blend(im, Image.new('RGB', im.size, (246, 242, 235)), .55)   # daylight: the project's colours, washed onto warm paper
    im.save(out); return out.as_uri()
def page(k):
    c, logo, lh, shot, kind, pos = D[k]
    L = (H / logo).as_uri()
    if kind == 'tilt':
        S = (H / shot).as_uri()
        body = f'<img class="atmo" src="{atmo(k, shot)}"><div class="win"><div class="bar"><i></i><i></i><i></i></div><img src="{S}" style="--pos:{pos}"></div><div class="shade"></div><div class="edge"></div><div class="chip"><img src="{L}" style="--lh:{lh}px"></div>'
    elif kind == 'full':
        body = f'<img class="full" src="{(H / shot).as_uri()}" style="--pos:{pos}"><div class="shade"></div><div class="edge"></div><div class="chip"><img src="{L}" style="--lh:{lh}px"></div>'
    elif kind == 'phone':
        S = (H / shot).as_uri()
        body = f'<img class="atmo" src="{atmo(k, shot)}"><div class="phone"><img src="{S}"></div><div class="shade"></div><div class="edge"></div><div class="chip"><img src="{L}" style="--lh:{lh}px"></div>'
    else:
        body = f'<div class="brand" style="background:radial-gradient(75% 55% at 50% 45%,{c}55,{c}18 45%,transparent 78%),linear-gradient(170deg,#FAF7F2,#EFE8DE)"></div><div class="edge"></div><div class="chip center"><img src="{L}" style="--lh:{lh}px"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
async def main():
    async with async_playwright() as p:
        br = await p.chromium.launch(args=['--disable-gpu', '--disable-gpu-rasterization', '--disable-features=TiledRasterization'])
        pg = await br.new_page(viewport={'width': W, 'height': HT}, device_scale_factor=2)
        for k in D:
            tmp = H / f'_deck_{k}.html'; tmp.write_text(page(k))
            await pg.goto(tmp.as_uri()); await pg.wait_for_timeout(250)
            png = H / f'_deck_{k}.png'; await pg.screenshot(path=str(png))
            # 1080 wide (sharp on 3x phones) + a whisper of grain so the soft blurred glow never bands into blocks
            im = Image.open(png).convert('RGB').resize((1080, 1440), Image.LANCZOS)
            a = np.asarray(im).astype(np.float32); rng = np.random.default_rng(7)
            a += rng.normal(0, 2.2, a.shape[:2])[..., None]
            Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(OUT / f'{k}.webp', 'WEBP', quality=90, method=6, use_sharp_yuv=True)
            tmp.unlink(); png.unlink()
            for f in H.glob(f'_atmo_{k}.png'): f.unlink()
        await br.close()
    print('deck cards:', sorted(x.name for x in OUT.iterdir()))
asyncio.run(main())
