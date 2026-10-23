import re
src=open('old_stripped.html').read()
# photo placeholders in player order
keys=['bibishkov','ciccarelli','tavernier','bruno','olguin','keshavarz','greco','campagna','pavela']
for k in keys: src=src.replace("photo:'B64'","photo:IMG.%s"%k,1)
assert 'B64' not in src

css_start=src.index('<style>')+7; css_end=src.index('</style>')
css=src[css_start:css_end]; rest_head=src[:css_start]; body=src[css_end:]

SKIP=['.site-footer','.footer-','.timezone-bar','.tz-','.social-link','.canada-flag','.prefooter','.top-ticker','.marquee-track','.red-ticker','.ts','.xi-node-tooltip','.cursor-','#xiSvg','amb-file','amb-bar','amb-progress','amb-redacted','amb-hint','.dot']
HEX={'#050505':'#F6F3EE','#0a0a14':'#F9F6F1','#080810':'#F6F3EE','#0d0d18':'#FBF9F5','#0a0a0a':'#F6F3EE','#0a0508':'#FBF3F2','#0d0d0d':'#FFFFFF','#130a0a':'#FCF4F3','#0d0a0d':'#FFFFFF','#130a13':'#FBF2F3','#07090a':'#F3F1EC','#08080f':'#F6F3EE','#0f0f1a':'#FBF9F5','#090909':'#F6F3EE','#0c0808':'#FBF3F2','#111111':'#FFFFFF','#0f0f0f':'#FFFFFF'}
def ta(a):
    if a>=0.5: return max(0.80,min(0.92,a+0.1))
    if a>=0.2: return 0.68
    return round(a*1.3,3)
def ba(a):
    if a<0.1: return 0.12
    if a<0.2: return 0.18
    return min(0.6,a+0.25)
def rgba_sub(prop,val):
    def f(m):
        r,g,b,a=int(m.group(1)),int(m.group(2)),int(m.group(3)),float(m.group(4))
        white = r>240 and g>240 and b>240
        dark = r<35 and g<35 and b<35
        if not(white or dark): return m.group(0)
        if prop in('color','fill','-webkit-text-fill-color'):
            return 'rgba(18,18,18,%s)'%ta(a) if white else m.group(0)
        if prop.startswith('border') or prop=='outline':
            return 'rgba(18,18,18,%s)'%ba(a) if white else m.group(0)
        if prop.startswith('background'):
            if white: return '#FFFFFF' if a<=0.06 else 'rgba(18,18,18,%s)'%round(min(a,0.5),3)
            return 'rgba(255,255,255,%s)'%max(a,0.85)
        if prop in('box-shadow','text-shadow','filter','stroke'):
            if white: return 'rgba(18,18,18,%s)'%round(a*0.3,3)
            return 'rgba(40,20,20,%s)'%round(a*0.3,3)
        return m.group(0)
    return re.sub(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)',f,val)
def decl_tx(sel,body):
    if any(s in sel for s in SKIP): return body
    out=[]
    for d in body.split(';'):
        if ':' not in d: out.append(d); continue
        p,v=d.split(':',1); prop=p.strip().lower()
        for h,l in HEX.items(): v=re.sub(re.escape(h)+r'\b',l,v,flags=re.I)
        if prop.startswith('background'): v=re.sub(r'#000(000)?\b','#FFFFFF',v)
        v=rgba_sub(prop,v)
        if prop=='color' and re.fullmatch(r'\s*(#fff|#ffffff|white)\s*(!important)?\s*',v,re.I) and '.btn-primary' not in sel:
            v=re.sub(r'(#fff(fff)?|white)','var(--c-white)',v,flags=re.I)
        out.append(p+':'+v)
    return ';'.join(out)
css=re.sub(r'([^{}]+)\{([^{}]*)\}',lambda m:m.group(1)+'{'+decl_tx(m.group(1),m.group(2))+'}',css)
# tokens
css=css.replace('--c-black:   #050505;','--c-black:   #F6F3EE;').replace('--c-deep:    #0a0a0a;','--c-deep:    #FFFFFF;')
css=css.replace('--c-panel:   #0f0f0f;','--c-panel:   #FFFFFF;').replace('--c-white:   #FFFFFF;','--c-white:   #121212;\n  --c-on-red:  #FFFFFF;\n  --c-ink-2:   #3A3A3A;\n  --c-muted:   #5E5E5E;')
css=css.replace('--c-gray:    #111111;','--c-gray:    #FFFFFF;').replace('--c-border:  rgba(255,255,255,0.08);','--c-border:  rgba(18,18,18,0.12);')

# ---- inline styles in HTML + JS (outside protected regions) ----
def protect(s):
    regs=[]
    for a,b in [('<svg id="xiSvg"','</svg>'),('<div class="prefooter-cta"','</footer>'),('<div class="top-ticker"','</div>\n\n<aside'),('<div class="red-ticker-wrap"','<section id="pipeline"'),('<div class="amb-file-overlay">','<!-- LOCKED STATE')]:
        i=s.find(a); j=s.find(b,i)
        if i>=0 and j>=0: regs.append((i,j+len(b)))
    return regs
regs=protect(body)
def inline_tx(seg):
    def f(m):
        prop=m.group(1).lower(); return m.group(1)+':'+rgba_sub(prop,m.group(2))
    seg=re.sub(r'(color|background(?:-color)?|border(?:-[a-z]+)?)\s*:\s*(rgba\([^)]*\))',f,seg)
    seg=re.sub(r'color:\s*#fff(fff)?\b','color:var(--c-white)',seg,flags=re.I)
    seg=seg.replace("background:#000","background:#EFEAE2")
    return seg
out=[];last=0
for i,j in sorted(regs):
    out.append(inline_tx(body[last:i])); out.append(body[i:j]); last=j
out.append(inline_tx(body[last:]))
body=''.join(out)
open('work.html','w').write(rest_head+css+body)
print('ok')
