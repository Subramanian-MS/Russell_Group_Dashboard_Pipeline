"""Adds per-university subject and salary detail to the dashboard data (reads the sliced Dash_* tables)."""
import pandas as pd, json, re, sys
DATA=sys.argv[1] if len(sys.argv)>1 else 'dash/data2.json'; OUT=sys.argv[2] if len(sys.argv)>2 else 'dash/data3.json'; DASH=sys.argv[3] if len(sys.argv)>3 else 'dash'; PROV=sys.argv[4] if len(sys.argv)>4 else 'out/Dim_Provider.csv'
d=json.load(open(DATA)); Y=d['year']; P=pd.read_csv(PROV,dtype=str); uk={v:k for k,v in zip(P.UKPRN,P.Provider)}
W=['Full-time employment','Part-time employment','Unknown pattern of employment','Voluntary or unpaid work','Employment and further study']
s=pd.read_csv(f'{DASH}/Dash_Subject.csv',dtype={'UKPRN':str}); s=s[s.Year==Y]; s['Subject']=s.Subject.str.replace(r'^\d\d ','',regex=True)
sp=s.pivot_table(index=['UKPRN','Subject'],columns='Activity',values='Number',aggfunc='sum').fillna(0)
sl=pd.read_csv(f'{DASH}/Dash_Salary.csv',dtype={'UKPRN':str}); sl=sl[sl.Year==Y]; sb=sl.pivot_table(index='UKPRN',columns='Salary_Band',values='Number',aggfunc='sum').fillna(0)
raw=lambda b:b.replace('<','Less than ').replace('–',' - ')
for u in d['unis']:
    k=uk[u['u']]; u['sj']={}
    for name,_ in d['subj']:
        if (k,name) in sp.index:
            r=sp.loc[(k,name)]; kn=sum(r[c] for c in r.index if c not in ('Total','Total with known outcomes','Non-respondents')); u['sj'][name]=[round(r[W].sum()/kn,4) if kn else 0,int(kn)]
    if k in sb.index and sb.loc[k,'Total']>0:
        t=sb.loc[k,'Total']; u['sal']=[round(sb.loc[k,raw(b)]/t,4) for b,_ in d['sal']]; u['sn']=int(t)
    else: u['sal']=None; u['sn']=0
rr=pd.read_csv('out/Fact_ResponseRate.csv',dtype={'UKPRN':str}); rr=rr[(rr.Year==Y)&(rr.Domicile_Detail=='All')&(rr.Level_Detail=='All')].set_index('UKPRN').Response_Rate
fa=pd.read_csv('out/Fact_Activity_Sex.csv',dtype={'UKPRN':str}); fa=fa[(fa.Year==Y)&(fa.Domicile=='All')&(fa.Level=='All')&(fa.Mode=='All')&(fa.Sex=='All')&(fa.Interim=='Include significant interim study')]
pv=fa.pivot_table(index='UKPRN',columns='Activity',values='Number',aggfunc='sum')
for u in d['unis']: u['pub']=round(float(rr[uk[u['u']]]),4)
d['rg']['pub']=round(float(pv['Total with known outcomes'].sum()/pv['Total'].sum()),4)
json.dump(d,open(OUT,'w'),separators=(',',':'))
print(len(open(OUT).read()),'bytes;', sum(1 for u in d['unis'] if u['sn']>=23),'universities with >=23 salary graduates;',sum(1 for u in d['unis'] for v in u['sj'].values() if v[1]<23),'subject cells under 23')
