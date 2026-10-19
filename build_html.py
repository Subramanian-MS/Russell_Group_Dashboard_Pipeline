"""Builds the dashboard HTML from the template, the data JSON and the validation report."""
import sys,re,datetime
tpl,data,rep,out=sys.argv[1:5]
t=open(tpl,encoding='utf-8').read(); r=open(rep,encoding='utf-8').read()
rows=[l for l in r.splitlines() if l.startswith('| ') and ('PASS' in l or 'REVIEW' in l)]
import html
rs=[[c.strip() for c in l.strip().strip('|').split('|')] for l in rows]
ch='<table class="vt"><thead><tr><th>Check</th><th>HESA table</th><th>Rule</th><th>Max difference</th><th>Tolerance</th><th>Result</th></tr></thead><tbody>'+''.join('<tr><td>'+'</td><td>'.join(html.escape(x) for x in (c[0],c[1],c[2],c[4],c[5],c[6]))+'</td></tr>' for c in rs)+'</tbody></table>'
t=t.replace('__CHECKS__',ch).replace('__DATA__',open(data).read()).replace('__BUILD__',datetime.date.today().strftime('%d %B %Y').lstrip('0')).replace('__NCHK__',str(len(rows))).replace('__NPASS__',str(sum('PASS' in l for l in rows)))
open(out,'w',encoding='utf-8').write(t); print('built',out,len(t),'bytes;',len(rows),'checks')
