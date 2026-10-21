# Statiske konsistenssjekker: tokens, referanser, klasser, filer, fargetabell og kontrast.
# Leser bare filene (ingen nettleser). Kjøres fra repo-roten eller hvor som helst: python3 .github/qa/statisk.py
import re,os,sys,glob
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
R=lambda f: open(f).read()
tok,comp,sty,idx,des,rd,th,yml=[R(f) for f in ['tokens.css','components.css','styles.css','index.html','DESIGN.md','README.md','header.js','.github/workflows/pages.yml']]
fails=[]
def ok(c,m):
	print(('  ok  ' if c else '  !!  ')+m)
	if not c: fails.append(m)
vals=lambda b: dict((k,v.strip()) for k,v in re.findall(r'(--[a-z0-9-]+):\s*([^;]+);',b))
dark=tok.split(':root {',1)[1].split('\n}',1)[0]
mq=re.search(r'@media \(prefers-color-scheme: light\) \{\n\t:root:not\(\[data-theme="dark"\]\) \{(.*?)\n\t\}\n\}',tok,re.S).group(1)
dl=re.search(r':root\[data-theme="light"\] \{(.*?)\n\}',tok,re.S).group(1)
D,M,L=vals(dark),vals(mq),vals(dl); A={**D,**M}
print('A. Tokens')
ok(M==L,f'lys-blokkene identiske ({len(M)} tokens hver)')
ok(set(M)<=set(D),'alle lys-overstyringer finnes i mørk blokk')
ok(len(D)==len(re.findall(r'(--[a-z0-9-]+):',dark)),'ingen duplikate definisjoner')
print(f'  {len(set(D)|set(M))} unike tokens')
print('B. Referanser')
local={'--alert-color','--alert-bg','--site-width','--on','--mx','--my'}
und=sorted({(f,u) for f,t in {'components':comp,'styles':sty,'index':idx,'tokens':tok}.items() for u in re.findall(r'var\((--[a-z0-9-]+)',t) if u not in D and u not in M and u not in local})
ok(not und,f'alle var(--x) er definert {und}')
used=set(re.findall(r'var\((--[a-z0-9-]+)',comp+sty+idx+tok))
ok(not [x for x in D if x not in used],f'alle tokens er i bruk: {[x for x in D if x not in used]}')
short={'--text-xs','--text-sm','--text-base','--text-lg','--text-xl','--text-2xl','--text-3xl','--space-1','--space-2','--space-3','--space-4','--space-5','--space-6','--space-7','--color-error-bg','--color-success-bg','--color-warning-bg','--color-info-bg','--color-accent-fill-hover'}
undoc=[x for x in D if not any(x in t for t in (des,idx)) and x not in short]
ok(not undoc,f'alle tokens er dokumentert: {undoc}')
print('C. Klasser')
strip=lambda s: re.sub(r'\{[^}]*\}','',re.sub(r'/\*.*?\*/','',s,flags=re.S))
cc=set(re.findall(r'\.([a-z][a-z0-9-]*)',strip(comp))); sc=set(re.findall(r'\.([a-z][a-z0-9-]*)',strip(sty)))
used_cls={c for u in re.findall(r'class="([^"]*)"',idx+th) for c in u.split()}
ok(not [c for c in used_cls if c not in cc|sc and c not in ('htmx-indicator','info')],'alle klasser i guiden er definert (unntatt htmx-indicator/info, standard)')
ok(not [c for c in sc if c not in used_cls and c not in cc and not c.startswith(('htmx','is-'))],'ingen ubrukte klasser i styles.css')
ok(not [c for c in cc if c not in used_cls and not c.startswith('htmx')],f'alle bibliotekklasser har demo i guiden: {[c for c in cc if c not in used_cls and not c.startswith("htmx")]}')
print('D. Filer og publisering')
refs=set(re.findall(r'(?:href|src)="([^"#?]+\.(?:css|js))',idx))
ok(all(os.path.exists(r) for r in refs),f'index.html peker på eksisterende filer {sorted(refs)}')
cp=re.search(r'cp (index.html[^\n]*) _site/',yml).group(1).split()
ok(refs<=set(cp)|{'index.html'},f'pages.yml kopierer alt guiden trenger')
sedl=re.findall(r'-e "s\|(?:href|src)=\\"([a-z.]+)',yml)
ok({r for r in refs}<=set(sedl),f'cache-busting dekker {sedl}')
ok(all(os.path.exists(f) for f in re.findall(r"url\('([^']+)'\)",tok)),'fontfiler finnes')
ok(all(os.path.exists(x) for x in re.findall(r'`((?:DESIGN|README|AGENTS)\.md|tokens\.css|components\.css|index\.html)`',des+rd)),'filer nevnt i DESIGN.md/README finnes')
# F-I
# Ikoner: filene må finnes og fargene må følge tokens (fil-ikoner kan ikke lese CSS-variabler)
icons=re.findall(r'<link rel="(?:icon|apple-touch-icon)" href="([^"]+)"',idx)
ok(len(icons)==3 and all(os.path.exists(i) for i in icons),f'ikon-lenker i index.html peker på eksisterende filer {icons}')
fill=re.search(r'fill="(#[0-9a-fA-F]{6})"',R('brand/favicon.svg'))
ok(bool(fill) and fill.group(1).lower()==D['--color-accent-fill'].lower(),f'brand/favicon.svg bruker --color-accent-fill ({D["--color-accent-fill"]})')
png=open('brand/apple-touch-icon.png','rb').read()
import zlib,struct
ct=png[25]; ch=3 if ct==2 else 4 if ct==6 else 0
pos,chunks=8,b''
while pos<len(png):
	n=struct.unpack('>I',png[pos:pos+4])[0]
	if png[pos+4:pos+8]==b'IDAT': chunks+=png[pos+8:pos+8+n]
	pos+=12+n
first=zlib.decompress(chunks)[1:1+ch] if ch else b''  # første piksel er uavhengig av PNG-filter
ok(ch>0 and '#%02x%02x%02x'%tuple(first[:3])==D['--color-bg'].lower(),f'brand/apple-touch-icon.png har mørk --color-bg ({D["--color-bg"]}) som bakgrunn')
ok('cp -r brand' in yml,'pages.yml kopierer brand/')
need=sorted(os.path.basename(f) for f in glob.glob('fonts/*')+glob.glob('brand/*'))
kig=des.split('## Kom i gang',1)[1].split('\n## ',1)[0] if '## Kom i gang' in des else ''
ok(bool(kig) and all(n in kig for n in need),f'«Kom i gang» i DESIGN.md nevner alle filer i fonts/ og brand/ {[n for n in need if n not in kig]}')
LT={**D,**L}
want={'brand/favicon.svg':set(),'brand/logo-lys-bakgrunn.svg':{LT['--color-text']},'brand/logo-mork-bakgrunn.svg':{D['--color-text']}}
for f in sorted(glob.glob('brand/*.svg')):
	svg=R(f); root=re.search(r'<svg[^>]*>',svg).group(0)
	bad=[t for t in ('<image','base64','shape-rendering','clip-path','<mask','<filter','@import','<text','<style') if t in svg]
	ok(not bad and 'viewBox' in root and not re.search(r'\s(width|height)=',root),f'{f}: ren vektor med viewBox og uten faste mål {bad}')
	fills={x.lower() for x in re.findall(r'fill="(#[0-9a-fA-F]{6})"',svg)}
	ok(f in want and fills=={D['--color-accent-fill'].lower()}|{c.lower() for c in want[f]},f'{f}: farger følger tokens {sorted(fills)}')
pl=re.search(r'\.logo-panel-light \{ background: (#[0-9a-fA-F]{6})',sty); pd=re.search(r'\.logo-panel-dark \{ background: (#[0-9a-fA-F]{6})',sty)
ok(bool(pl and pd) and pl.group(1).lower()==LT['--color-bg'].lower() and pd.group(1).lower()==D['--color-bg'].lower(),'logo-panelene i styles.css har --color-bg for lys og mørk modus')
tl=re.search(r'\.icon-tab-light \{ background: (#[0-9a-fA-F]{6}); color: (#[0-9a-fA-F]{6})',sty); td=re.search(r'\.icon-tab-dark \{ background: (#[0-9a-fA-F]{6}); color: (#[0-9a-fA-F]{6})',sty)
ok(bool(tl and td) and [x.lower() for x in tl.groups()]==[LT['--color-bg'].lower(),LT['--color-text'].lower()] and [x.lower() for x in td.groups()]==[D['--color-bg'].lower(),D['--color-text'].lower()],'fane-eksemplene i styles.css har --color-bg og --color-text for lys og mørk modus')
tc=dict((mm,v.lower()) for v,mm in re.findall(r'<meta name="theme-color" content="(#[0-9a-fA-F]{6})" media="\(prefers-color-scheme: (dark|light)\)">',idx))
ok(tc=={'dark':D['--color-bg'].lower(),'light':LT['--color-bg'].lower()},f'theme-color i index.html følger --color-bg ({tc})')
key=re.search(r"localStorage\.getItem\('([^']+)'\)",idx); tkey=re.search(r'data-theme-toggle data-theme-key="([^"]+)"',idx)
ok(bool(key and tkey) and key.group(1)==tkey.group(1),'tema-nøkkelen i <head>-scriptet er den samme som data-theme-key på temabryteren')
ok(D['--color-bg'].lower() in des.lower() and LT['--color-bg'].lower() in des.lower(),'DESIGN.md nevner hex for theme-color (mørk og lys --color-bg)')
print('E. Fargetabellen i guiden mot tokens.css')
def parse(v):
	v=v.strip(); m=re.match(r'#([0-9a-f]{6})$',v)
	if m: h=m.group(1); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),1.0)
	m=re.match(r'rgba?\(([^)]*)\)',v)
	if m: p=[float(x) for x in m.group(1).split(',')]; return (p[0],p[1],p[2],p[3] if len(p)>3 else 1.0)
lin=lambda c:(lambda x: x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4)(c/255)
Lm=lambda r:0.2126*lin(r[0])+0.7152*lin(r[1])+0.0722*lin(r[2])
over=lambda f,b: tuple(f[i]*f[3]+b[i]*(1-f[3]) for i in range(3))
def cr(a,b): x,y=sorted([Lm(a),Lm(b)],reverse=True); return (x+0.05)/(y+0.05)
rows=re.findall(r'<tr><td><code>(--[^<]+)</code></td><td class="col-dark">(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',idx)
Lg={**D,**L}
bad=[]
for t,dc,lc,use in rows:
	if '*' in t or t=='--color-link': continue
	for mode,cell,src in (('mørk',dc,D),('lys',lc,Lg)):
		m=re.search(r'</span>(#[0-9a-f]{6}|rgba\([^)]*\))</span>$',cell) or re.search(r'^(rgba\([^)]*\))$',cell)
		s=m.group(1) if m else None
		s2=re.sub(r'(?<=,)\.(\d+)\)',r'0.\1)',s) if s else s
		a=tuple(round(x,2) for x in parse(s2)) if s2 else None; b=tuple(round(x,2) for x in parse(src[t]))
		if a!=b: bad.append((t,mode,s,src[t]))
ok(not bad,f'{len(rows)} tabellrader stemmer med tokens.css {bad}')
miss=[k for k in D if k.startswith('--color-') and k not in {r[0] for r in rows} and not re.match(r'--color-(error|success|warning|info)-bg',k)]
ok(not miss,f'alle fargetokens står i tabellen {miss}')
print('F. Kontrast fra tokens.css')
col=lambda mode,t: parse((D if mode=='mørk' else Lg)[t])
bad=[]
for mode in ('mørk','lys'):
	bg=col(mode,'--color-bg')[:3]; sf=col(mode,'--color-surface')[:3]
	for t in ['--color-text','--color-text-secondary','--color-text-muted','--color-label','--color-accent','--color-accent-hover','--color-error','--color-success','--color-warning','--color-info']:
		f=col(mode,t); r=min(cr(over(f,bg),bg),cr(over(f,sf),sf))
		if r<4.5: bad.append((mode,t,round(r,2)))
	for a,b in [('--color-on-accent','--color-accent-fill'),('--color-on-accent','--color-accent-fill-hover'),('--color-bg','--color-error')]:
		r=cr(col(mode,a)[:3],col(mode,b)[:3])
		if r<4.5: bad.append((mode,a,b,round(r,2)))
	e=col(mode,'--color-error'); x=col(mode,'--color-text'); h=tuple(e[i]*.85+x[i]*.15 for i in range(3))
	if cr(col(mode,'--color-bg')[:3],h)<4.5: bad.append((mode,'btn-danger:hover'))
	for t in ['--color-border-control','--color-accent-border']:
		f=col(mode,t); r=min(cr(over(f,bg),bg),cr(over(f,sf),sf))
		if r<3.0: bad.append((mode,t,round(r,2)))
	for t in ['--color-accent','--color-error']:
		f=col(mode,t); r=min(cr(f[:3],bg),cr(f[:3],sf))
		if r<3.0: bad.append((mode,t,'fokus',round(r,2)))
ok(not bad,f'tekst ≥4,5:1 og UI/fokus ≥3:1 i begge moduser (inkl. btn-danger hover) {bad}')
bad=[]
for t,dc,lc,use in rows:
	m=re.search(r'([\d,]+):1 / ([\d,]+):1',use)
	if m and t in ('--color-text','--color-text-secondary','--color-text-muted','--color-label','--color-accent','--color-accent-hover','--color-error','--color-success','--color-warning','--color-info'):
		cd,cl=[float(x.replace(',','.')) for x in m.groups()]
		rd=cr(over(col('mørk',t),col('mørk','--color-bg')[:3]),col('mørk','--color-bg')[:3]); rl=cr(over(col('lys',t),col('lys','--color-bg')[:3]),col('lys','--color-bg')[:3])
		if abs(rd-cd)>0.06 or abs(rl-cl)>0.06: bad.append((t,cd,cl,round(rd,2),round(rl,2)))
ok(not bad,f'kontrasttall i tabellen stemmer (±0,06) {bad}')
bad=[]
for mode in ('mørk','lys'):
	tint=col(mode,'--color-accent-bg-subtle')
	for base in ('--color-bg','--color-surface'):
		tb=over(tint,col(mode,base)[:3])
		for t in ['--color-text','--color-text-secondary','--color-text-muted','--color-label','--color-accent','--color-error','--color-success','--color-warning','--color-info']:
			r=cr(over(col(mode,t),tb),tb)
			if r<4.5: bad.append((mode,base,t,round(r,2)))
ok(not bad,f'tekst ≥4,5:1 på hover-tint (--color-accent-bg-subtle) over bg og surface {bad}')
print('\nSTØRRELSER'); 
for f in ['DESIGN.md','AGENTS.md','README.md','tokens.css','components.css','styles.css','index.html']: print(f'  {f:18}{len(R(f).splitlines()):5} linjer')
print('\nRESULTAT:','ALLE STATISKE SJEKKER OK' if not fails else f'{len(fails)} FEIL: {fails}')
sys.exit(1 if fails else 0)
