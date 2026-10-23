import base64,re,sys
s=open('work3.html').read()
for k in ['bibishkov','ciccarelli','tavernier','bruno','olguin','keshavarz','greco','pavela']:
    s=s.replace('{{IMG:%s}}'%k,'data:image/webp;base64,'+base64.b64encode(open('heads_cut/%s.webp'%k,'rb').read()).decode())
s=s.replace('{{IMG:campagna}}','')
assert '{{IMG' not in s
s=s.replace('True_North_Ballers_Badge.png','data:image/png;base64,'+base64.b64encode(open('assets/badge200.png','rb').read()).decode())
open('../site/index.html','w').write(s)
js=re.findall(r'<script>(.*?)</script>',s,re.S)
open('work-check.js','w').write('\n'.join(js))
print(len(s),'bytes')
