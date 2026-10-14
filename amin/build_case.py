import base64,re,sys
b=lambda f,m:f'data:{m};base64,'+base64.b64encode(open(f,'rb').read()).decode()
def build(video_src):
    t=open('case.html').read()
    def sub(m):
        k=m.group(1)
        if k=='LOGO': return b('out/logo.png','image/png')
        if k=='POSTER': return b('out/poster.jpg','image/jpeg')
        if k=='VIDEOSRC': return video_src
        return b(f'out/{k}.webp','image/webp')
    return re.sub(r'\{\{([A-Za-z0-9_]+)\}\}',sub,t)
open('out/amin-case-study.html','w').write(build('amin-walkthrough.mp4'))
open('out/amin-case-embedded.html','w').write(build(b('out/amin-walkthrough-small.mp4','video/mp4')))
print('ok')
