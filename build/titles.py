import json,re
B=sorted(json.load(open('buildings_from_draft3.json')),key=lambda b:b['no'])
U={o['id']:o for o in json.load(open('current_use_merged.json'))}
D=json.load(open('denue_matches.json'))
T={ # id: tenant label shown in the title line, in brackets after the address
'RN-007':'Círculo Cubano de México social club','RN-252':'Sitio de Memoria Circular de Morelia, memorial site',
'RN-038':'Casa Universitaria del Libro, UNAM','RN-273':'Cantina La Covadonga','RN-272':'Deli Gallery',
'RN-275':'Revuelta Queer House, LGBTQ+ cultural centre','RN-047':'Ultramarinos Demar restaurant',
'RN-052':'Colegio México school','RN-062':'Lorea restaurant and Alelí Rooftop',
'RN-066':'Casa Museo Guillermo Tovar de Teresa','RN-080':'Casona Roma Norte hotel',
'RN-089':'Olivia Foundation private museum','RN-093':'Artes de México publishers','RN-105':'Gran Cantina Filomeno',
'RN-108':'Condesa DF hotel','RN-127':'Huset restaurant','RN-131':'MUCA Roma museum, UNAM',
'RN-284':'La Valise hotel','RN-255':'Nima Local House hotel',
'RN-132':'El Cortés hotel; Lotti restaurant','RN-142':'Centro Budista','RN-147':'Centro Gallego de México',
'RN-149':'Brick Hotel','RN-254':'Rosetta restaurant','RN-155':'MODO museum',
'RN-169':'Maison México Roma hotel; Xuna restaurant','RN-279':'Arróniz Arte Contemporáneo gallery',
'RN-266':'Casa Franca jazz bar','RN-264':'Casa Virginia restaurant','RN-199':'El Parián shopping arcade',
'RN-203':'Casa Lamm cultural centre','RN-207':'Casa del Poeta Ramón López Velarde','RN-210':'La Docena oyster bar',
'RN-251':'Casa Estudio Leonora Carrington museum, UAM','RN-214':'Instituto Renacimiento school','RN-217':'Casa Prunes restaurant',
'RN-261':'Casa Goliana guesthouse','RN-224':'Universidad de Londres','RN-287':'Broka Bistrot restaurant',
'RN-227':'Universidad de la Comunicación','RN-229':'Casa Rafael Galván cultural centre, UAM','RN-288':'Foro Indie Rocks concert venue',
'RN-268':'M.N. Roy club','RN-238':'Plaza Insurgentes and Sears','RN-265':'Galanga Thai House restaurant',
'RN-240':'Universidad de Londres','RN-286':'Maison Celeste hotel','RN-269':'Terreno Baldío Arte gallery',
'RN-281':'Santa Casa hotel','RN-263':'Ignacia Guest House',
# new from INEGI DENUE 2026
'RN-233':'Monte Sinaí synagogue','RN-148':'Casa Tibet México cultural centre','RN-167':'Universidad de Londres',
'RN-235':'Universidad de Londres','RN-239':'Universidad de Londres','RN-241':'Universidad de Londres',
'RN-103':'Pigeon restaurant and Bar Las Brujas',
}
out=[]
for b in B:
    addr=b['title'].split(' · ')[0]
    import re as _re
    cur=_re.split(r'\n(?:Source notes|Protection|Sources)',b['current'] or '')[0].replace('\n',' ').strip() if b['current'] and 'Not yet' not in b['current'] else ''
    src='draft 3' if cur else ''
    if not cur:
        u=U[b['id']]
        if u['suggested']: cur=u['suggested'].replace('Mixed: ','Mixed use: ')+' (INEGI business directory, May 2026)'; src='INEGI'
        elif u['web']: cur=u['web'].split('] ',1)[1]; src='web'
    old=b['title'].split(' · ',1)[1] if ' · ' in b['title'] else ''
    out.append({'no':b['no'],'id':b['id'],'address':addr,'title':addr+(f" ({T[b['id']]})" if b['id'] in T else ''),'old_tenant':old,'current':cur,'current_source':src})
json.dump(out,open('titles_v4.json','w'),ensure_ascii=False,indent=1)
kept=[o for o in out if o['id'] in T and o['old_tenant']]; new=[o for o in out if o['id'] in T and not o['old_tenant']]; dropped=[o for o in out if o['old_tenant'] and o['id'] not in T]
print(len(kept),'kept',len(new),'new',len(dropped),'dropped')
print('DROPPED:'); [print(' ',o['address'],'—',o['old_tenant'][:50]) for o in dropped]
M={'RN-047':'Michelin Bib Gourmand','RN-062':'Alelí Rooftop: Michelin Bib Gourmand','RN-080':'Michelin Key','RN-284':'Michelin Key','RN-255':'Michelin Key','RN-132':'Lotti: in the Michelin Guide','RN-149':'Michelin Key','RN-254':'one Michelin star','RN-169':'Xuna: in the Michelin Guide','RN-261':'in the Michelin Guide','RN-265':'Michelin Bib Gourmand','RN-286':'Michelin Key','RN-281':'in the Michelin Guide','RN-263':'Michelin Key'}
for x in out:
    if x['id'] in M and M[x['id']].split(':')[-1].strip().lower() not in x['current'].lower():
        x['current']=(x['current'].rstrip('.')+'. ' if x['current'] else '')+M[x['id']][0].upper()+M[x['id']][1:]+'.'
json.dump(out,open('titles_v4.json','w'),ensure_ascii=False,indent=1)
