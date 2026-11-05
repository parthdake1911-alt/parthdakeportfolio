"""Build the All In case study: allin/case_src.html -> allin/index.html (images in allin/img/).
build_site.py copies allin/index.html and allin/img/ into site/allin/."""
import os
H = os.path.dirname(os.path.abspath(__file__))
n = [0]
P = 'M20 4H118a14 14 0 0 0 28 0H180a16 16 0 0 1 16 16V90a16 16 0 0 1-16 16H146a14 14 0 0 0-28 0H20A16 16 0 0 1 4 90V20A16 16 0 0 1 20 4Z'

def ticket(fill='#FFA45D', ink='#10262E', w=120, tilt=-8, label=True):
    n[0] += 1; i = f'bt{n[0]}'
    txt = (f'<text x="68" y="71" text-anchor="middle" font-family="Outfit, system-ui, sans-serif" font-weight="800" font-size="46" letter-spacing="-2" fill="{ink}">all</text>'
           f'<text x="166" y="71" text-anchor="middle" font-family="Outfit, system-ui, sans-serif" font-weight="800" font-size="46" letter-spacing="-2" fill="{ink}">in</text>') if label else ''
    return (f'<svg class="br-ticket" width="{w}" viewBox="-6 -6 212 122" role="img" aria-label="All In">'
            f'<defs><clipPath id="{i}"><path d="{P}"/></clipPath></defs><g transform="rotate({tilt} 100 55)"><path d="{P}" fill="{fill}"/>'
            f'<g clip-path="url(#{i})"><rect width="200" height="40" fill="#fff" opacity=".22"/><rect y="98" width="200" height="12" fill="{ink}" opacity=".10"/></g>'
            f'<line x1="132" y1="24" x2="132" y2="86" stroke="{ink}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 10" opacity=".85"/>{txt}</g></svg>')

def icon(size, bg='#10262E', fill='#FFA45D', shine=True):
    return (f'<span class="br-icon{" shine" if shine else ""}" style="width:{size}px;height:{size}px;border-radius:{round(size*.28)}px;background:{bg}">'
            f'{ticket(fill, "#10262E", round(size*.78), -10)}</span>')

def word(size, color='#10262E', dot='#FFA45D'):
    return f'<span class="br-word" style="font-size:{size}px;color:{color}">all <span class="br-i">ı<i style="background:{dot}"></i></span>n</span>'

marq = ''.join(f'<span>{t}</span><b>✦</b>' for t in ['Stop chasing', 'Lock the trip', 'Pay your share to say yes', 'Not enough? Everyone gets it back', '0 reminders from Neha', 'That’s a wrap'])
rep = {
    '%%ICON56%%': icon(56), '%%WORD34%%': word(34, '#10262E', '#fff'), '%%MARQ%%': marq,
    '%%TICKET60%%': ticket('#fff', '#10262E', 64, 0), '%%TICKETBIG%%': ticket('#fff', '#10262E', 200, -6),
    '%%TICKET44%%': ticket('#FFA45D', '#10262E', 48, 0, False),
    '%%ICON130%%': icon(130), '%%WORD54%%': word(54),
    '%%TICKETEL%%': ticket('#fff', '#10262E', 190, 0), '%%TICKETST%%': ticket('#FFA45D', '#10262E', 64, 0),
    '%%TICKETSW%%': ticket('#FFA45D', '#10262E', 38, 0, False),
}
s = open(f'{H}/case_src.html').read()
for k, v in rep.items():
    s = s.replace(k, v)
assert '%%' not in s, 'unfilled placeholder'
open(f'{H}/index.html', 'w').write(s)
print('built allin/index.html', len(s) // 1024, 'KB')
