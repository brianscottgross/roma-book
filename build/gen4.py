import json,html,re,os,glob
E=html.escape
P={d['kicker'].split('· ')[1]:d for d in json.load(open('data/pages_struct.json'))}
T=json.load(open('data/titles_v5.json'))
GMU=json.load(open('data/gm_use.json'))
chap=[('Av. Chapultepec',12),('Puebla',48),('Plaza de la Romita (group)',1),('Sinaloa',16),('Durango',31),('Plaza Río de Janeiro (group)',7),('Colima',64),('Tabasco',20),('Álvaro Obregón',29),('Chihuahua',8),('Guanajuato',10),('Plaza Luis Cabrera (group)',3),('Zacatecas',8),('Querétaro',6),('San Luis Potosí',11),('Chiapas',5),('Coahuila (north side)',6)]
css=open('build/page.html').read().split('<style>')[1].split('</style>')[0]
css=css.replace('.foot{position:fixed;bottom:-0.4in;width:100%;text-align:center;font-size:6pt}','')
css+='''
@page{size:Letter;margin:0.7in 0.85in;@bottom-center{content:counter(page);font:6pt 'Liberation Sans',sans-serif;color:#444}}
html{counter-reset:page 9}
.bld{break-before:page}
.chap{break-before:page}.chap h1{font-size:26pt;color:#9b1031;border-bottom:1px solid #333;padding-bottom:4px;margin-bottom:4px}
.chap .sub{font-family:'Liberation Sans';font-size:8.5pt;color:#777;margin-bottom:14px}
.chap ol{columns:2;column-gap:28px;font-size:9.5pt;padding-left:22px;margin:0}.chap li{break-inside:avoid;margin-bottom:2px}
.chap a{color:#9b1031;text-decoration:none}.chap .t{color:#222}
.subt{font-family:'Liberation Sans';font-size:11pt;color:#444;margin:-4px 0 8px}
.notes p{margin:0 0 4px}.dis{margin-top:6px;font-size:8.5pt}
.src a{color:#555}
.qh{font-family:Inter;font-weight:700;font-size:7.5pt;letter-spacing:.06em;color:#9b1031;margin-bottom:4px}.qn{font-family:"Liberation Sans";font-size:7pt;color:#888;font-style:italic}.quote p{margin:0 0 5px}.dem .kick{color:#555}li.dem{list-style:none;color:#666;font-style:italic}li.dem a{color:#666}.fns{margin-top:8px;border-top:.5pt solid #bbb;padding-top:3px}.fn{font-size:7pt;color:#444;line-height:1.3}.fn sup,.qh sup{font-size:5.5pt}
.sv{margin:6px 0 2px;break-inside:avoid}.sv img{width:100%;max-height:3.1in;object-fit:cover;object-position:center 60%;display:block}.mly{display:flex;gap:8px;margin:6px 0;break-inside:avoid}.mly figure{flex:1;margin:0}.mly img{width:100%;height:1.5in;object-fit:cover;display:block}.mly figcaption{font-family:'Liberation Sans';font-size:6pt;color:#888;margin-top:2px}
'''
D=json.load(open('data/denue_matches.json'))
SV={f.split('/')[-1][:-4]:f for f in glob.glob('data/streetview/*.jpg')}
MLY={}  # Mapillary removed (Street View only)
import collections
SMALL={'De','Del','La','Las','Los','Y','E','El','En','Para','Por','Sin','Con','A'}
def tc(n):
    w=n.strip().title().split()
    return ' '.join(x.lower() if i and x in SMALL else x for i,x in enumerate(w))
CAT=[('Hoteles','hotel'),('Pensiones y casas de hu','guest house'),('Restaurantes','restaurant'),('Bares','bar'),('Centros nocturnos','nightclub'),('Cafeter','café'),('Museos','museum'),('educación superior','university'),('educación media superior','school'),('educación preescolar','kindergarten'),('Escuelas de idiomas','language school'),('Escuelas','school'),('religiosas','religious organisation'),('Administración pública','government office'),('instituciones','public office'),('Bibliotecas','archive'),('Promotores del sector p','cultural venue'),('Bufetes','law firm'),('Notar','notary'),('Asociaciones','foundation'),('Servicios funerarios','funeral chapel'),('Consultorios','medical practice'),('belleza','beauty salon'),('Comercio al por menor','shop'),('Comercio al por mayor','office'),('Servicios','office')]
def cat(a):
    for k,v in CAT:
        if k in a: return v
    return 'business'
MICH={'RN-047':'Michelin Bib Gourmand','RN-062':'Alelí Rooftop: Michelin Bib Gourmand','RN-080':'Michelin Key','RN-284':'Michelin Key','RN-255':'Michelin Key','RN-132':'Lotti: in the Michelin Guide','RN-149':'Michelin Key','RN-254':'one Michelin star','RN-169':'Xuna: in the Michelin Guide','RN-261':'in the Michelin Guide','RN-265':'Michelin Bib Gourmand','RN-286':'Michelin Key','RN-281':'in the Michelin Guide','RN-263':'Michelin Key'}
def current_line(t,v,u):
    if not (u or 'Not yet checked' in v):
        out=v
    else:
        ents=D[t['id']]['denue']; seen=collections.OrderedDict()
        for e in ents: seen.setdefault(tc(e['nom_estab']),cat(e['nombre_act']))
        if seen:
            items=list(seen.items()); shown=items[:4]
            out=('; '.join(f'{n} ({c})' for n,c in shown)+(f'; and {len(items)-4} more' if len(items)>4 else '')+' (INEGI business directory, May 2026)')
            if len(items)>1: out='Several businesses: '+out
        elif t['current_source']=='web': out=t['current']
        else: out=''
    if not out and not GMU.get(t['id']):
        return ('No businesses listed at this address on Google Maps (Oct 2026)',False) if t['id'] in GMU else (v,u)
    g=GMU.get(t['id'])
    if g:
        gl='; '.join(f"{e['name']} ({re.sub(r'\b(mexican|italian|japanese|spanish|cuban|argentinian|asian|buddhist)\b',lambda m:m.group(1).title(),e['cat'].lower())})" for e in g)
        out=out.rstrip('. ')+('. ' if out else '')+f'Google Maps lists at this address: {gl} (Google Maps, Oct 2026).'
    m=MICH.get(t['id'])
    if m and m.split(':')[-1].strip().lower() not in out.lower(): out=out.rstrip('. ')+'. '+m[0].upper()+m[1:]+'.'
    return out,False
def cell(v,u): return f'<td class="u">{E(v)}</td>' if u else f'<td>{E(v)}</td>'
def maplink(d):
    for l in d['links']:
        if 'google.com/maps' in l['uri']: return l['uri']
def srclinks(d,txt):
    t=E(txt)
    for l in d['links']:
        u=l['uri']
        if 'google.com/maps' in u: continue
        dom=re.sub(r'^https?://','',u).split('/')[0]
        if dom in t and f'href="{u}"' not in t:
            t=t.replace(dom,f'<a href="{E(u)}">{dom}</a>',1)
    return t
TAV={}
for _f in ('A','B'):
    for _b in json.load(open(f'data/tavares/trans{_f}.json')): TAV[_b['id']]=[x for x in _b['items'] if x['relevance']!='none' and x['en']]
TCIT='Edgar Tavares López, <i>Colonia Roma</i>, Barrios y colonias de la Ciudad de México nº 1 (Mexico City: Clío), Kindle edition, loc. {loc}.'
def tav_block(bid,start=1):
    its=TAV.get(bid,[])
    if not its: return '',''
    q=[];fn=[]
    for k,it in enumerate(its,start):
        lab='From the source' if it['relevance']=='main' else 'Mention in the source'
        paras=''.join(f'<p>{E(p)}</p>' for p in it['en'].split('\n') if p.strip())
        q.append(f'<div class="quote"><div class="qh">{lab} · Tavares, <i>Colonia Roma</i> (Clío) · translated from Spanish<sup>{k}</sup></div>{paras}<div class="qn">Working note: full translation kept for research. To be rewritten in our own words before publication.</div></div>')
        fn.append(f'<div class="fn"><sup>{k}</sup> {TCIT.format(loc=it["loc"])}</div>')
    return ''.join(q),'<div class="fns">'+''.join(fn)+'</div>'
DEM={e['id']:e for e in json.load(open('data/tavares/demolished/trans.json'))}
DEMMETA={
'D01':('RN-276','after','Site of the Toreo de la Condesa','Durango and Salamanca (south-east corner) · bullring, 1907–1946'),
'D02':('RN-094','after','Site of a Porfirian residence, Durango 90','Corner of Córdoba'),
'D03':('RN-102','after','Site of a residence, Orizaba 43','Corner of Plaza Río de Janeiro'),
'D04':('RN-025','before','Site of the Austro-Hungarian ambassador’s residence, Jalapa 12',''),
'D05':('RN-042','after','Site of the Lamm chalet, Córdoba 42',''),
'D06':('RN-038','after','Site of Leopoldo Gout’s house','Almost opposite the Sagrada Familia church (exact address not given)'),
'D07':('RN-125','before','Site of two residences at Insurgentes and Colima','Including the Robles Gil family house'),
'D08':('RN-156','before','Site of Córdoba 86','Lost in the 1985 earthquake'),
'D09':('RN-192','before','Site of General Álvaro Obregón’s house, Álvaro Obregón 185','Then Avenida Jalisco 185'),
'D10':('RN-201','after','Site of a mansion at Álvaro Obregón and Orizaba','South-west corner'),
'D11':('RN-217','after','Chihuahua 72','Named in the account of the 1985 earthquake'),
'D12':('RN-220','before','Site of the Cine Royal','Corner of Mérida and Guanajuato'),
'D13':('RN-233','before','Site of Querétaro 171','Lost in the 1985 earthquake'),
'D14':('RN-246','after','Site of Chiapas 61a','Lost in the 1985 earthquake')}
DEMFIX={'D10':{'architect':'—','note':'Possibly the house built by the Spaniard Eusebio González (“el Burro de Oro”), which a resident remembered at Obregón y Orizaba; Tavares does not say they are the same house.'},
 'D11':{'note':'Tavares names Chihuahua 72 as the ruinous “neighbour” that destroyed Chiapas 61a, but the two addresses are about five blocks apart, so the passage is unclear.'},
 'D14':{'note':'Tavares says Chiapas 61a was destroyed by its neighbour “Chihuahua 72”; the two addresses are about five blocks apart, so the neighbour may be misnamed in the source.'}}
DEMNOW={'D09':'A mid-century multi-storey building with shops (Street View, Oct 2024)','D11':'A parking lot behind a gate numbered 72 (Street View, Sep 2024)','D13':'Street View near the address (Dec 2024) shows a fenced vacant lot'}
DQ={'D01': 'Durango y Salamanca', 'D02': 'Durango 90', 'D03': 'Orizaba 43', 'D04': 'Jalapa 14', 'D05': 'Córdoba 42', 'D07': 'Insurgentes y Colima', 'D08': 'Córdoba 86', 'D09': 'Álvaro Obregón 185', 'D10': 'Álvaro Obregón y Orizaba', 'D11': 'Chihuahua 72', 'D12': 'Mérida y Guanajuato', 'D13': 'Querétaro 171', 'D14': 'Chiapas 61'}
def dem_section(did):
    e=DEM[did]; after,_,title,sub=DEMMETA[did]; fx=DEMFIX.get(did,{})
    h=[f'<section class="bld dem" id="{did}"><div class="kick">DEMOLISHED · SITE</div><h1>{E(title)}</h1>']
    if sub: h.append(f'<div class="subt">{E(sub)}</div>')
    sv=SV.get(did)
    if sv: h.append(f'<div class="sv"><img src="{sv}"><div class="cap"><a href="https://www.google.com/maps/search/?api=1&amp;query={_u.quote_plus(DQ[did]+', Roma Norte, Ciudad de México')}">Google Street View</a> (screenshot) · what stands on the site today</div></div>')
    now=e['now'] if e['now']!='—' else DEMNOW.get(did,'—')
    rows=[('Built',e['built']),('Architect / builder',fx.get('architect',e['architect'])),('Lost',e['lost']),('On the site now',now)]
    h.append('<table>'+''.join(f'<tr><td class="k">{E(k)}</td>'+(f'<td class="u">{E(v)}</td>' if v=='—' else f'<td>{E(v)}</td>')+'</tr>' for k,v in rows)+'</table>')
    if fx.get('note'): h.append(f'<div class="dis"><b>Note:</b> {E(fx["note"])}</div>')
    q=[];fn=[]
    for k,it in enumerate(e['items'],1):
        paras=''.join(f'<p>{E(p)}</p>' for p in it['en'].split('\n') if p.strip())
        q.append(f'<div class="quote"><div class="qh">From the source · Tavares, <i>Colonia Roma</i> (Clío) · translated from Spanish<sup>{k}</sup></div>{paras}<div class="qn">Working note: full translation kept for research. To be rewritten in our own words before publication.</div></div>')
        fn.append(f'<div class="fn"><sup>{k}</sup> {TCIT.format(loc=it["loc"])}</div>')
    h.append(''.join(q)+'<div class="fns">'+''.join(fn)+'</div></section>')
    return ''.join(h)
DEMAT={}
for _d,(_rid,_pos,_t,_s) in DEMMETA.items(): DEMAT.setdefault((_rid,_pos),[]).append(_d)
import urllib.parse as _u
GQ={q['id']:'https://www.google.com/maps/search/?api=1&query='+_u.quote_plus(q['q']+', Roma Norte, Ciudad de México') for q in json.load(open('data/streetview/meta/queries.json'))}
GM={}
for _l in open('data/streetview/meta/gm.tsv'):
    _p=_l.rstrip('\n').split('\t')
    if len(_p)>=3 and _p[1]: GM[_p[0]]=(_p[1],_p[2])
VER={}
if os.path.exists('data/streetview/meta/verified_panos.tsv'):
    for _l in open('data/streetview/meta/verified_panos.tsv'):
        _p=_l.rstrip('\n').split('\t')
        if len(_p)>=3: VER[_p[0]]=(_p[1],_p[2])
def svlink(i):
    if i in VER: return f'https://www.google.com/maps/@?api=1&map_action=pano&pano={VER[i][0]}&heading={VER[i][1]}'
    return GQ.get(i,'https://www.google.com/maps')
def building(t):
    d=P[t['id']]
    h=[f'<section class="bld" id="{t["id"]}"><div class="kick">NO. {t["no"]} · {t["id"]}</div><h1>{E(t["title"])}</h1>']
    if d['subtitle']: h.append(f'<div class="subt">{E(d["subtitle"])}</div>')
    if d.get('photo'): h.append(f'<div class="ph"><img src="{E(d["photo"])}"></div><div class="cap">{E(d["photo_caption"])}</div>')
    sv=SV.get(t['id'])
    if sv: h.append(f'<div class="sv"><img src="{sv}"><div class="cap"><a href="{E(svlink(t['id']))}">Google Street View</a> (screenshot) · reference for your own photo, not for publication</div></div>')
    mc=[]  # Mapillary removed per Brian
    if mc: h.append('<div class="mly">'+''.join(f'<figure><img src="{c[0]}"><figcaption>Mapillary · {E(c[1] or "contributor")}, {c[2]} · CC BY-SA 4.0</figcaption></figure>' for c in mc)+'</div>')
    m=GQ.get(t['id']) or maplink(d); loc=d['location'].replace(' · Google Maps',' · <a href="%s">Google Maps</a>'%E(m or '#'),1) if 'Google Maps' in d['location'] else E(d['location'])
    if loc.strip()=='Google Maps': loc=f'<a href="{E(m)}">Google Maps</a>'
    loc=loc.replace('</a> (approximate)','</a>')
    loc=re.sub(r'^(.*?)( · <a)',lambda x:E(x.group(1))+x.group(2),loc) if '<a' in loc else loc
    h.append(f'<div class="loc">{loc}</div>')
    h.append('<table>'+''.join(f'<tr><td class="k">{E(k)}</td>{cell(v,u)}</tr>' for k,v,u in d['rows'])+'</table><h2>USES</h2><table>')
    for k,v,u in d['uses']:
        if k=='Current':
            v,u=current_line(t,v,u)
        h.append(f'<tr><td class="k">{E(k)}</td>{cell(v,u)}</tr>')
    h.append('</table>')
    if d['notes']: h.append(f'<div class="notes"><b>Source notes:</b> {srclinks(d,d["notes"])}</div>')
    if d['disagree']: h.append(f'<div class="dis"><b>Sources disagree:</b> {E(d["disagree"])}</div>')
    src=d['sources']
    if 'INEGI business directory' in ''.join(h) and 'INEGI' not in src: src+=' · INEGI DENUE (May 2026)'
    h.append(f'<div class="src"><b>Sources:</b> {srclinks(d,src)}</div>')
    if t['id']!='RN-044':
        q,fn=tav_block(t['id']); h.append(q+fn)
    return h
body=[];i=0
for name,n in chap:
    grp=T[i:i+n]; i+=n
    body.append(f'<section class="chap"><h1>{E(name.replace(" (group)",""))}</h1><div class="sub">{n} {"building" if n==1 else "buildings"}, west to east</div><ol start="{grp[0]["no"]}">')
    for t in grp:
        a=t['title']; addr,ten=(a.split(' (',1)+[''])[:2]
        for _d in DEMAT.get((t['id'],'before'),[]): body.append(f'<li class="dem"><a href="#{_d}">† {E(DEMMETA[_d][2])}</a></li>')
        body.append(f'<li value="{t["no"]}"><a href="#{t["id"]}">{E(addr)}</a>'+(f' <span class="t">({E(ten)}</span>' if ten else '')+'</li>')
        for _d in DEMAT.get((t['id'],'after'),[]): body.append(f'<li class="dem"><a href="#{_d}">† {E(DEMMETA[_d][2])}</a></li>')
        if t['id']=='RN-044': body.append('<li value="47"><a href="#P109">Puebla 109 (Orizaba 27) · conjunto</a></li>')
    body.append('</ol></section>')
    for t in grp:
        for _d in DEMAT.get((t['id'],'before'),[]): body.append(dem_section(_d))
        h=building(t)
        if t['id']=='RN-044':
            h=[x for x in h]
            hh=''.join(h)
            hh=hh.replace('<td class="u">Unknown</td></tr><tr><td class="k">Architect</td><td class="u">Unknown</td></tr><tr><td class="k">Style</td><td class="u">Not stated in sources</td>','<td>1921</td></tr><tr><td class="k">Architect</td><td>Eudoro Urdaneta and Julio Corredor Latorre</td></tr><tr><td class="k">Style</td><td>Carries on the ornament of the 1910s (per source)</td>')
            hh=hh.replace('<td>Residence (per typology in source)</td>','<td>Stately urban residence (residencia señorial urbana)</td>')
            hh=hh.replace('Tavares 2015, pp. 106','Tavares 2015, pp. 103–104, 106')
            body.append(hh+open('build/frag_quote.html').read().replace('Tavares 2015, pp. 103–104 · translated from Spanish','Tavares 2015, pp. 103–104 · translated from Spanish<sup>1</sup>')+'<div class="fns"><div class="fn"><sup>1</sup> Same passage in '+TCIT.format(loc='756')+'</div></div></section>')
            p109=open('build/frag_p109.html').read().replace('<div class="kick" style="break-before:page">NEW ENTRY · AFTER NO. 47 · CONJUNTO OF THREE</div>','<section class="bld" id="P109"><div class="kick">NO. 47A · NEW ENTRY · CONJUNTO OF THREE</div>')
            p109=p109.replace('<tr><td class="k">Current use</td><td class=u>Not yet checked</td></tr></table>\n<div class="notes">Stone corner','<tr><td class="k">Current use</td><td>Sarde restaurant (INEGI business directory, May 2026)</td></tr></table>\n<div class="notes">Stone corner',1)
            body.append(p109+'</section>')
        else:
            body.append(''.join(h)+'</section>')
        for _d in DEMAT.get((t['id'],'after'),[]): body.append(dem_section(_d))
doc=f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>'+'\n'.join(body)+'</body></html>'
doc=doc.replace('<section class="chap">','<section class="chap" style="break-before:auto">',1)
open('out/book.html','w').write(doc)
print(len(doc))
