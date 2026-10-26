#!/usr/bin/env python3
"""Try to find Müller (Vancouver Whitecaps kit) and Sánchez (CF Montréal kit) on Wikimedia Commons."""
import json, urllib.request, urllib.parse, re
UA = 'tnballers.com photo fetcher (contact@tnballers.com)'
def jget(url):
    r = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(r, timeout=20) as resp:
        return json.load(resp)

def search_commons(query, limit=5):
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({
        'action':'query','format':'json','generator':'search',
        'gsrsearch':query,'gsrnamespace':6,'gsrlimit':limit,
        'prop':'imageinfo','iiprop':'url|user|extmetadata','iiurlwidth':800
    })
    try:
        d = jget(url)
    except Exception as e:
        print('ERR', e); return []
    pages = d.get('query',{}).get('pages',{})
    results = []
    for pid, p in pages.items():
        ii = (p.get('imageinfo') or [{}])[0]
        md = ii.get('extmetadata',{})
        lic = md.get('LicenseShortName',{}).get('value','')
        results.append({
            'title': p.get('title',''),
            'url': ii.get('url',''),
            'thumb': ii.get('thumburl',''),
            'desc': ii.get('descriptionurl',''),
            'licence': lic,
            'author': re.sub(r'<[^>]+>','', md.get('Artist',{}).get('value','')).strip()[:60],
        })
    return results

for q in [
    'Thomas Muller Vancouver Whitecaps',
    'Thomas Muller MLS',
    'Alexis Sanchez CF Montreal',
    'Alexis Sanchez Montreal',
    'Alexis Sanchez MLS 2026',
]:
    print(f'=== {q} ===')
    for r in search_commons(q, 5):
        print(f"  {r['licence']:18}  {r['title']}  by {r['author']}")
