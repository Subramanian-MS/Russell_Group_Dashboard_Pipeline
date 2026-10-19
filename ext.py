import pandas as pd, json
d=json.load(open('dash/data.json')); P=pd.read_csv('out/Dim_Provider.csv',dtype=str); nm=dict(zip(P.UKPRN,P.Provider))
a=pd.read_csv('dash/Dash_Activity.csv',dtype={'UKPRN':str}); o=pd.read_csv('dash/Dash_Occupation.csv',dtype={'UKPRN':str})
W=['Full-time employment','Part-time employment','Unknown pattern of employment','Voluntary or unpaid work','Employment and further study']
S=['Full-time further study','Part-time further study','Unknown pattern of further study','Employment and further study']
p=a.pivot_table(index=['UKPRN','Year'],columns='Activity',values='Number',aggfunc='sum').fillna(0)
k=p['Total with known outcomes']; p['work']=p[W].sum(axis=1)/k; p['study']=p[S].sum(axis=1)/k; p['unemp']=p['Unemployed']/k
yrs=d['trend']['years']; Y=d['year']
mixc=['Full-time employment','Part-time employment','Unknown pattern of employment','Voluntary or unpaid work','Employment and further study','Full-time further study','Part-time further study','Unknown pattern of further study','Other including travel, caring for someone or retired','Unemployed']
q=o.pivot_table(index=['UKPRN','Year'],columns='SOC',values='Number',aggfunc='sum').fillna(0)
def sk(r): t=r['Total']-r['Unknown']; return [round(r['Total high skilled']/t,4),round(r['Total medium skilled']/t,4),round(r['Total low skilled']/t,4)]
for u in d['unis']:
    uk=[i for i,n in nm.items() if n==u['u']][0]
    u['n']=int(p.loc[(uk,Y),'Total']); u['tr']=[[round(p.loc[(uk,y),m],4) for y in yrs] for m in ['work','study','unemp']]
    u['mix']=[int(p.loc[(uk,Y),c]) for c in mixc]; u['sk']=sk(q.loc[(uk,Y)])
tot=q.xs(Y,level='Year').sum(); d['sk']=sk(tot); d['mixk']=mixc
json.dump(d,open('dash/data2.json','w'),separators=(',',':'))
# cross-check vs HESA published percentages (table 6)
c=pd.read_csv('out/Fact_Activity_CI.csv',dtype={'UKPRN':str})
c=c[(c.Year==Y)&(c.Domicile=='All')&(c.Level=='All')&(c.Mode=='All')&(c.Interim=='Exclude significant interim study')]
pc=c.pivot_table(index='UKPRN',columns='Activity',values='Percent',aggfunc='first')
pw=pc[W].sum(axis=1); pu=pc['Unemployed']
mine=p.xs(Y,level='Year')
print('max |work diff| pp:',round(((mine.work-pw).abs().max())*100,2),' max |unemp diff| pp:',round(((mine.unemp-pu).abs().max())*100,2))
print('mean diffs',round((mine.work-pw).abs().mean()*100,2),round((mine.unemp-pu).abs().mean()*100,2))
import os;print(os.path.getsize('dash/data2.json'))
