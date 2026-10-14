import base64,re
b=open('body.html').read(); css=open('../anchor/base_style.css').read()+open('extra.css').read(); js=open('../anchor/base_script.js').read()
js=js.replace("""      else if (href === 'amin-prototype.html') { e.preventDefault(); parent.postMessage({ pd: 'proto' }, '*'); }""","")
page=f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UltraTech Cement – Case Study · Parth Dake</title>
<meta name="description" content="A guided mobile experience for the home-building journey, with Hindi and English audio guidance. Client project by Parth Dake.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
{b}
<script>{js}</script>
</body>
</html>"""
open('case.html','w').write(page)
enc=lambda f,m:f'data:{m};base64,'+base64.b64encode(open(f,'rb').read()).decode()
def sub(m):
    k=m.group(1)
    return enc('../cards/logo.png','image/png') if k=='LOGO' else enc(f'out/{k}.webp','image/webp')
open('out/preview.html','w').write(re.sub(r'\{\{([A-Za-z0-9_]+)\}\}',sub,page)); print('built')
