import asyncio, sys, json; sys.path.insert(0,'/home/claude/ica/tools')
from run import *
BASE=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8777/'
SIZES=[(1440,900,False),(390,844,True)] if len(sys.argv)<3 else [tuple(int(x) for x in s.split('x'))+(True,) for s in sys.argv[2].split(',')]
fails=[]
def ok(name,cond,info=''):
    print(('PASS ' if cond else 'FAIL ')+name+(' '+str(info) if info and not cond else ''))
    if not cond: fails.append(name)
async def check_case(p, folder, w, h, mob):
    b = await p.chromium.launch(); ctx=await b.new_context(viewport={'width':w,'height':h}, is_mobile=mob, has_touch=mob)
    pg=await ctx.new_page(); await pg.route('**/*', route)
    errs=[]; bad=[]
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.on('response', lambda r: bad.append(f'{r.status} {r.url}') if r.status>=400 else None)
    await pg.goto(BASE+folder+'/'); await pg.wait_for_timeout(800)
    H=await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0,H,500): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(40)
    # force lazy images in horizontal strips too
    await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
    await pg.wait_for_timeout(1500)
    r=await pg.evaluate('''({imgs:[...document.images].filter(i=>i.getAttribute('src')).map(i=>[i.getAttribute('src'),i.complete&&i.naturalWidth>0]),
        sw:document.documentElement.scrollWidth, iw:innerWidth, fonts:[...document.fonts].filter(f=>f.status==='loaded').length,
        noDims:[...document.images].filter(i=>i.getAttribute('src')&&!i.getAttribute('width')&&!i.closest('.lb')).map(i=>i.getAttribute('src')),
        nav:[...document.querySelectorAll('.nav a')].map(a=>a.getAttribute('href')), video:[...document.querySelectorAll('video source')].map(s=>s.getAttribute('src'))})''')
    broken=[s for s,o in r['imgs'] if not o]
    tag=f'{folder} {w}px'
    ok(f'{tag}: {len(r["imgs"])} images load', not broken, broken)
    ok(f'{tag}: no horizontal scroll', r['sw']<=r['iw']+1, (r['sw'],r['iw']))
    ok(f'{tag}: no console/page errors', not errs, errs[:3])
    ok(f'{tag}: no failed requests', not bad, bad[:3])
    ok(f'{tag}: fonts loaded', r['fonts']>0)
    ok(f'{tag}: every image has width/height', not r['noDims'], r['noDims'][:3])
    ok(f'{tag}: nav links', r['nav']==['../#work','../#about','../#contact'], r['nav'])
    if folder=='amin': ok(f'{tag}: video is MP4 only', r['video']==['walkthrough.mp4'], r['video'])
    await b.close()
async def main():
    async with async_playwright() as p:
        for f in ['amin','anchor','ica','tatapower','casagrand']:
            for w,h,m in SIZES:
                await check_case(p,f,w,h,m)
    print('FAILS:',len(fails), fails)
asyncio.run(main())
