"""Apply Parth's design assets to the Customer Smile screens (source files and the bundled prototype):
- 'The step I took was…' gets its own illustration (a person with a checklist)
- 'Help me write' gets the pen, 'Speak instead' gets the microphone (both occurrences)
- the bottom navigation follows the new nav bar design: glass bar with 12px corners, line icons in slate,
  the active tab as a soft blue pill with its label, a red count badge on Rewards."""
import re, base64, json, os
H = os.path.dirname(os.path.abspath(__file__))
b64 = lambda n: 'data:image/png;base64,' + base64.b64encode(open(f'{H}/src/assets/{n}.png', 'rb').read()).decode()
PEN, MIC, STEP = b64('pen'), b64('mic'), b64('step')
ICON = {  # line icons from bottom-nav-bar.svg, moved into a 24x24 box
 'Home': '<svg class="nsv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><g transform="translate(-42 -31.5)"><path d="M57 52.9992V44.9992C57 44.734 56.8946 44.4796 56.7071 44.2921C56.5196 44.1046 56.2652 43.9992 56 43.9992H52C51.7348 43.9992 51.4804 44.1046 51.2929 44.2921C51.1054 44.4796 51 44.734 51 44.9992V52.9992M45 41.9997C44.9999 41.7088 45.0633 41.4213 45.1858 41.1574C45.3082 40.8935 45.4868 40.6595 45.709 40.4717L52.709 34.4717C53.07 34.1666 53.5274 33.9992 54 33.9992C54.4726 33.9992 54.93 34.1666 55.291 34.4717L62.291 40.4717C62.5132 40.6595 62.6918 40.8935 62.8142 41.1574C62.9367 41.4213 63.0001 41.7088 63 41.9997V50.9997C63 51.5301 62.7893 52.0388 62.4142 52.4139C62.0391 52.789 61.5304 52.9997 61 52.9997H47C46.4696 52.9997 45.9609 52.789 45.5858 52.4139C45.2107 52.0388 45 51.5301 45 50.9997V41.9997Z"/></g></svg>',
 'Explore': '<svg class="nsv" viewBox="0 0 24 24" fill="currentColor"><g transform="translate(-100 -32)"><path d="M112 32C105.382 32 100 37.382 100 44C100 50.618 105.382 56 112 56C118.618 56 124 50.618 124 44C124 37.382 118.618 32 112 32ZM112 33.6C117.753 33.6 122.4 38.2467 122.4 44C122.4 49.7533 117.753 54.4 112 54.4C106.247 54.4 101.6 49.7533 101.6 44C101.6 38.2467 106.247 33.6 112 33.6Z"/><path d="M115.703 39.2578L109.989 41.5437C109.786 41.6251 109.625 41.786 109.544 41.989L107.258 47.7016C107.093 48.1116 107.292 48.5775 107.702 48.7422C107.893 48.8191 108.107 48.8191 108.298 48.7422L114.011 46.4562C114.214 46.3753 114.376 46.2143 114.458 46.0109L116.742 40.2969C116.905 39.8862 116.705 39.421 116.294 39.2578C116.104 39.1823 115.893 39.1823 115.703 39.2578ZM114.562 41.4359L113.098 45.0984L109.437 46.5624L110.903 42.9015L114.562 41.4359Z"/></g></svg>',
 'Rewards': '<svg class="nsv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><g transform="translate(-215 -32)"><path d="M218 36L220.303 50.077C220.422 50.8061 220.742 51.4879 221.225 52.0467C221.708 52.6056 222.337 53.0196 223.041 53.243L223.369 53.347C225.732 54.097 228.268 54.097 230.631 53.347L230.959 53.243C231.663 53.0196 232.292 52.6056 232.775 52.0467C233.258 51.4879 233.578 50.8061 233.697 50.077L236 36"/><path d="M236 36C236 37.1046 231.971 38 227 38C222.029 38 218 37.1046 218 36C218 34.8954 222.029 34 227 34C231.971 34 236 34.8954 236 36Z"/></g></svg>',
 'Awards': '<svg class="nsv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><g transform="translate(-271 -32)"><path d="M281 46.6604V48.2865C280.996 48.6292 280.904 48.9651 280.733 49.2621C280.562 49.5591 280.318 49.8072 280.024 49.9826C279.399 50.4455 278.89 51.0477 278.539 51.7414C278.188 52.4352 278.003 53.2013 277.999 53.979M285 46.6604V48.2865C285.004 48.6292 285.096 48.9651 285.266 49.2621C285.437 49.5591 285.682 49.8072 285.976 49.9826C286.601 50.4455 287.109 51.0477 287.461 51.7414C287.812 52.4352 287.997 53.2013 288 53.979M289 40.9998H290.5C291.164 40.9998 291.799 40.7364 292.268 40.2675C292.737 39.7986 293.001 39.1627 293.001 38.4996C293.001 37.8365 292.737 37.2005 292.268 36.7317C291.799 36.2628 291.164 35.9994 290.5 35.9994H289M289 40.9998C289 42.5912 288.368 44.1174 287.243 45.2427C286.117 46.3681 284.591 47.0002 283 47.0002C281.408 47.0002 279.882 46.3681 278.757 45.2427C277.632 44.1174 276.999 42.5912 276.999 40.9998M289 40.9998V35.9994M289 35.9994V34.9993C289 34.734 288.895 34.4797 288.707 34.2921C288.52 34.1046 288.265 33.9992 288 33.9992H277.999C277.734 33.9992 277.48 34.1046 277.292 34.2921C277.105 34.4797 276.999 34.734 276.999 34.9993V35.9994M276.999 40.9998V35.9994M276.999 40.9998H275.499C274.836 40.9998 274.2 40.7364 273.731 40.2675C273.262 39.7986 272.999 39.1627 272.999 38.4996C272.999 37.8365 273.262 37.2005 273.731 36.7317C274.2 36.2628 274.836 35.9994 275.499 35.9994H276.999M274.999 54.0008H291"/></g></svg>',
 'Profile': '<svg class="nsv" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><g transform="translate(-327 -32)"><path d="M346.001 53V51C346.001 49.9391 345.579 48.9217 344.829 48.1716C344.079 47.4214 343.061 47 342 47H335.999C334.938 47 333.921 47.4214 333.171 48.1716C332.42 48.9217 331.999 49.9391 331.999 51V53M343 39C343 41.2091 341.209 43 339 43C336.79 43 334.999 41.2091 334.999 39C334.999 36.7909 336.79 35 339 35C341.209 35 343 36.7909 343 39Z"/></g></svg>',
}
NAV_CSS = '''<style id="nav-v2">
/* bottom nav: Parth's nav bar design */
.nav{border-radius:12px !important;height:64px !important;padding:8px !important;
  background:linear-gradient(176deg,rgba(255,255,255,.72),rgba(244,255,247,.5)) !important;border:1px solid #fff !important;
  -webkit-backdrop-filter:blur(16px) !important;backdrop-filter:blur(16px) !important;
  box-shadow:0 8px 30px -10px rgba(29,97,225,.18),inset 0 1px 0 rgba(255,255,255,.8) !important}
.nav > div:first-child{border-radius:12px !important}
.nav-ind{top:8px !important;height:48px !important;border-radius:12px !important;background:#EAF1FE !important}
.nt{border-radius:12px !important;padding:0 14px !important;color:#5B6472}
.nt.on{color:#195EBE;gap:8px !important}
.ni img{display:none !important}
.ni .nsv{width:24px;height:24px;display:block}
.nl{font-size:16px !important;font-weight:500 !important;color:#195EBE !important;letter-spacing:-.01em}
.nt.on .nl{max-width:90px !important}
.nbadge{top:-6px !important;right:-6px !important;min-width:14px !important;height:14px !important;line-height:14px !important;font-size:9px !important;border:0 !important;background:#FF5257 !important}
/* form helpers: Parth's illustrations */
.aid{height:60px !important;border-radius:16px !important;justify-content:flex-start !important;gap:10px !important;padding:0 14px !important;
  background:linear-gradient(180deg,rgba(255,255,255,.95),rgba(244,255,247,.7)) !important;border:1px solid rgba(29,97,225,.14) !important;
  color:#16202C !important;font-size:15px !important;font-weight:500 !important;white-space:nowrap !important;text-align:left !important}
.aid.js-ai{color:#0E6E73 !important;border-color:rgba(14,110,115,.55) !important;background:linear-gradient(180deg,#fff,rgba(234,248,246,.8)) !important}
.aid img{width:40px !important;height:40px !important;border-radius:0 !important;mix-blend-mode:normal !important;object-fit:contain}
.q-ic.art{background:none !important;border-radius:12px !important}
.q-ic.art img{object-fit:contain !important}
</style>'''
def patch(h):
    if 'id="nav-v2"' in h:   # already applied: refresh the stylesheet only
        return re.sub(r'<style id="nav-v2">.*?</style>', lambda m: NAV_CSS, h, flags=re.S)
    # nav icons
    def nav_btn(m):
        t = m.group(2); svg = ICON.get(t)
        return m.group(1) + re.sub(r'(<span class="ni">)', r'\1' + svg, m.group(3), count=1) if svg else m.group(0)
    h = re.sub(r'(<button class="nt[^"]*" data-t="(\w+)"[^>]*>)(.*?</button>)', nav_btn, h, flags=re.S)
    # form helpers
    h = re.sub(r'(<button class="aid tap js-ai"><img alt="" src=")[^"]+(")', r'\g<1>' + PEN + r'\2', h)
    h = re.sub(r'(<button class="aid tap js-speak"><img alt="" src=")[^"]+(")', r'\g<1>' + MIC + r'\2', h)
    h = re.sub(r'(<section class="q" data-q="step">\s*<div class="q-h"><div class="q-ic)(">)<img alt="" src="[^"]+"',
               r'\1 art\2<img alt="" src="' + STEP + '"', h)
    return h.replace('</head>', NAV_CSS + '\n</head>', 1)

SPIN_CSS = """<style id="spin-v2">
/* daily spin: a clear ending — what you won, one button to collect it, and when the next spin unlocks */
.sheet{max-height:100%;overflow-y:auto}
@media (max-height:720px){.sheet .wheel-wrap{zoom:.82;margin:10px auto 8px}}
@media (max-height:620px){.sheet .wheel-wrap{zoom:.68}}
.spin-result.win{font-size:17px !important;line-height:24px;color:#0f1b2d !important;background:linear-gradient(135deg,rgba(0,134,50,.1),rgba(25,94,190,.1));border-radius:14px;padding:10px 14px;margin:0 4px}
.spin-btn.collect{opacity:1 !important;cursor:pointer !important;box-shadow:0 10px 22px -10px rgba(25,94,190,.7) !important}
.spin-next{font-size:12px;color:var(--mute);text-align:center;margin-top:10px;min-height:16px;font-variant-numeric:tabular-nums}
.spin-card.used .spin-cta{background:rgba(0,134,50,.1) !important;color:#008632 !important;font-weight:600}
.spin-card.used .spin-card-s{color:#0f1b2d}
</style>"""
def patch_spin(h):
    if 'id="spin-v2"' in h:
        return re.sub(r'<style id="spin-v2">.*?</style>', lambda m: SPIN_CSS, h, flags=re.S)
    if 'class="spin-btn"' not in h: return h
    rep = [
      ('<button class="spin-btn">Spin now</button>', '<button class="spin-btn">Spin now</button>\n        <p class="spin-next" aria-live="polite"></p>'),
      ("$('.spin-btn').text('Next spin in '+hh+':'+mm+':'+ss);", "$('.spin-next').text('Next spin unlocks in '+hh+':'+mm+':'+ss);"),
      ("var hub=$('.hub')[0]; burstAt(hub); startCountdown(); }});",
       "var hub=$('.hub')[0]; burstAt(hub); startCountdown();"
       " won=prizes[i][0]; $('.spin-btn').prop('disabled',false).addClass('collect').text('Collect & close');"
       " $('.spin-card').addClass('used'); $('.spin-cta').text('Collected'); $('.spin-card-s').text('You won '+won+' today'); }});"),
      ("var weights=[22,20,8,12,6,16,6,10], rot=0, busy=false, used=false;", "var weights=[22,20,8,12,6,16,6,10], rot=0, busy=false, used=false, won='';"),
      ("$('.spin-btn,.hub').on('click',spin);",
       "$('.hub').on('click',spin); $('.spin-btn').on('click',function(){ if(!used){ spin(); return; }"
       " if(window.closeSheet) closeSheet(); setTimeout(function(){ if(window.toast) toast('Collected: '+won); },350); });"),
      ("var mo=new MutationObserver(function(){ var t=$('.sheet .spin-btn').text(); if(/Next spin/.test(t)){ $('.spin-card').addClass('used'); $('.spin-cta').text(t.replace('Next spin in ','')); $('.spin-card-s').text('Next spin unlocks at midnight'); } });",
       "var mo=new MutationObserver(function(){});"),
    ]
    for a, b in rep:
        assert a in h, a[:60]
        h = h.replace(a, b, 1)
    return h.replace('</head>', SPIN_CSS + '\n</head>', 1)

if __name__ == '__main__':
    for f in sorted(os.listdir(f'{H}/src/screens')):
        p = f'{H}/src/screens/{f}'; s = open(p).read(); n = patch_spin(patch(s)); open(p, 'w').write(n); print(f, 'changed' if n != s else 'same')
    p = f'{H}/src/mcs.html'; src = open(p).read()
    sm = re.search(r'(<script id="screens" type="application/json">)(.*?)(</script>)', src, re.S)
    sc = json.loads(sm.group(2))
    for k, v in sc.items():
        sc[k] = base64.b64encode(patch_spin(patch(base64.b64decode(v).decode())).encode()).decode()
    open(p, 'w').write(src[:sm.start(2)] + json.dumps(sc) + src[sm.end(2):]); print('mcs.html bundled screens patched')
