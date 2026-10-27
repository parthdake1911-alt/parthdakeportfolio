import asyncio, sys; sys.path.insert(0,'/home/claude/ica/tools')
from run import *
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8777/'
SP='/tmp/claude-0/-home-claude/056a394b-02b8-5f93-a710-c26895cbb183/scratchpad/'
fails=[]
def ok(n,c,i=''):
    print(('PASS ' if c else 'FAIL ')+n+(' '+str(i) if i and not c else '')); 
    if not c: fails.append(n)
async def main():
    async with async_playwright() as p:
        for w,h,m,tag in [(1440,900,False,'desk'),(390,844,True,'mob')]:
            b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':w,'height':h},is_mobile=m,has_touch=m)
            pg=await ctx.new_page(); await pg.route('**/*', route)
            errs=[]; bad=[]; ext=set()
            pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda x: errs.append(x.text) if x.type=='error' else None)
            pg.on('response', lambda r: bad.append(f'{r.status} {r.url}') if r.status>=400 else None)
            pg.on('request', lambda r: ext.add(r.url.split('/')[2]) if not r.url.startswith(BASE) and r.url.startswith('http') else None)
            await pg.goto(BASE); await pg.wait_for_timeout(3500)
            await pg.screenshot(path=SP+f'qa_{tag}_hero.png')
            ok(f'{tag}: hero has no video, motion pill present', await pg.evaluate("!document.querySelector('#hero video') && !!document.querySelector('#hero .ph2 .canvas')"))
            sc=await pg.evaluate("document.getElementById('scroller').offsetHeight - innerHeight")
            await pg.evaluate(f"scrollTo(0,{sc})"); await pg.wait_for_timeout(3500); await pg.screenshot(path=SP+f'qa_{tag}_work.png')
            cards=await pg.evaluate("[...document.querySelectorAll('a.card')].map(a=>[a.getAttribute('aria-label'),a.querySelector('img').currentSrc.split('/').pop()])")
            ok(f'{tag}: 6 cards with deck images', len(cards)==6 and all(c[1].split('?')[0].endswith('.webp') for c in cards), cards)
            for sel in ['#about','#contact']:
                await pg.evaluate(f"document.querySelector('{sel}').scrollIntoView()"); await pg.wait_for_timeout(2500)
                await pg.screenshot(path=SP+f'qa_{tag}_{sel[1:]}.png')
            imgs=await pg.evaluate("[...document.images].filter(i=>i.getAttribute('src')&&!i.closest('#lightbox')).map(i=>[i.getAttribute('src').slice(0,40),i.complete&&i.naturalWidth>0])")
            ok(f'{tag}: homepage images load', all(o for _,o in imgs), [s for s,o in imgs if not o])
            ok(f'{tag}: lightbox photo not loaded until opened', await pg.evaluate("!document.querySelector('#lightbox img').getAttribute('src')"))
            if tag=='desk':
                await pg.locator('#convo').click(); await pg.wait_for_timeout(1500)
                ok('desk: lightbox photo loads on open', await pg.evaluate("(()=>{const i=document.querySelector('#lightbox img');return i.complete&&i.naturalWidth>0})()"))
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(500)
                href=await pg.evaluate("document.getElementById('ctResume').getAttribute('href')")
                r=await pg.request.get(BASE+href); ok('résumé link works', r.status==200 and r.headers['content-type']=='application/pdf', (href,r.status))
                # nav links
                for name,want in [('About','about'),('Contact','contact'),('Work','scroller')]:
                    await pg.locator('.nav a.lnk',has_text=name).first.click(); await pg.wait_for_timeout(1600)
                    y=await pg.evaluate('scrollY')
                    tgt=await pg.evaluate(f"Math.round(document.getElementById('{want}').getBoundingClientRect().top+scrollY)")
                    ok(f'nav {name} scrolls to its section', abs(y-tgt)<120 or (want=='scroller' and y>tgt), (y,tgt))
            ok(f'{tag}: no console/page errors', not errs, errs[:3]); ok(f'{tag}: no failed requests', not bad, bad[:3])
            ok(f'{tag}: no horizontal scroll', await pg.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
            print(f'   external hosts contacted: {sorted(ext)}')
            await b.close()
        b,pg=await page(p,1440,900,1,BASE+'404.html'); await pg.wait_for_timeout(800)
        ok('404 page renders with logo', await pg.evaluate("document.querySelector('h1').textContent=='Page not found' && document.querySelector('img').naturalWidth>0"))
        await pg.screenshot(path=SP+'qa_404.png'); await b.close()
    print('FAILS:',len(fails),fails)
asyncio.run(main())
