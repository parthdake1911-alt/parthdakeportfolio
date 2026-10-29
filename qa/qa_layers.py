import asyncio, sys; sys.path.insert(0,'/home/claude/ica/tools')
from run import *
BASE=sys.argv[1]
fails=[]
def ok(n,c,i=''):
    print(('PASS ' if c else 'FAIL ')+n+(' '+str(i) if i and not c else ''))
    if not c: fails.append(n)
CASES=[('Tata','#tatapower','Customer Smile working prototype'),('ICA','#ica','ICA redesigned homepage'),
       ('AMIN','#amin','AMIN member portal prototype'),('Anchor','#anchor','Anchor trading journal prototype'),('Casagrand','#casagrand','Casagrand homepage prototype')]
async def on(pg): return await pg.evaluate('[...document.querySelectorAll(".page-layer.on")].map(e=>e.getAttribute("aria-label"))')
async def main():
    async with async_playwright() as p:
        b,pg=await page(p,1440,900,1,BASE); await pg.wait_for_timeout(2000)
        errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        await pg.evaluate("scrollTo(0, document.getElementById('scroller').offsetHeight - innerHeight)"); await pg.wait_for_timeout(3500)
        for name,hash_,proto in CASES:
            await pg.evaluate(f"(()=>{{const cs=[...document.querySelectorAll('a.card')];const i=cs.findIndex(a=>a.getAttribute('aria-label').startsWith('{name}'));scrollTo(0,window.__deckTop(i));}})()"); await pg.wait_for_timeout(2500)
            bb=await pg.locator(f'a.card[aria-label^="{name}"] .go').bounding_box()
            await pg.mouse.move(bb['x']+5,bb['y']+5); await pg.wait_for_timeout(300)
            pf=await pg.evaluate("[...document.querySelectorAll('link[rel=prefetch]')].map(l=>l.getAttribute('href'))")
            await pg.mouse.click(bb['x']+bb['width']/2, bb['y']+bb['height']/2); await pg.wait_for_timeout(2200)
            layers=await on(pg)
            ok(f'{name}: card opens case study ({hash_})', len(layers)==1 and pg.url.endswith(hash_), (layers,pg.url))
            ok(f'{name}: case study prefetched on hover', any(hash_.strip('#')[:4] in x for x in pf), pf)
            fr=pg.frame_locator('.page-layer.on iframe').first
            if proto:
                await fr.locator('a[data-proto]').first.click(); await pg.wait_for_timeout(4500)
                layers=await on(pg); ok(f'{name}: prototype opens', proto in layers, layers)
                src=await pg.evaluate("(()=>{const l=[...document.querySelectorAll('.page-layer.on')].pop();const f=l.querySelector('iframe');try{return [f.src.split('/').slice(-2).join('/'), f.contentDocument.body.innerHTML.length]}catch(e){return [f.src,'x']}})()")
                ok(f'{name}: prototype content loaded', isinstance(src[1],int) and src[1]>200, src)
                await pg.locator('.page-layer.on .back').last.click(); await pg.wait_for_timeout(700)
                ok(f'{name}: back to case study', len(await on(pg))==1)
            await fr.locator('.foot a[href="../#work"]').click(); await pg.wait_for_timeout(1500)
            ok(f'{name}: "more projects" returns to the cards', len(await on(pg))==0)
        ok('homepage: no page errors during navigation', not errs, errs[:2])
        await b.close()
        for name,hash_,_ in CASES:
            b,pg=await page(p,1440,900,1,BASE+hash_); await pg.wait_for_timeout(2500)
            ok(f'deep link {hash_} opens directly', len(await on(pg))==1); await b.close()
    print('FAILS:',len(fails),fails)
asyncio.run(main())
