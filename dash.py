import pandas as pd, json, shutil
O='out/'; D='dash/'
P=pd.read_csv(O+'Dim_Provider.csv',dtype=str); nm=dict(zip(P.UKPRN,P.Provider))
rd=lambda f:pd.read_csv(O+f,dtype={'UKPRN':str})
X='Exclude significant interim study'
a=rd('Fact_Activity_Sex.csv'); a=a[(a.Domicile=='All')&(a.Level=='All')&(a.Mode=='All')&(a.Sex=='All')&(a.Interim==X)][['UKPRN','Year','Activity','Number']]
o=rd('Fact_Occupation.csv'); o=o[(o.Domicile=='All')&(o.Level=='All')&(o.Mode=='All')&(o.Work_Type=='All')][['UKPRN','Year','SOC','Number']]
s=rd('Fact_Subject.csv'); s=s[(s.Level=='All')&(s.Mode=='All')&(s.Interim==X)][['UKPRN','Year','Subject','Activity','Number']]
sl=rd('Fact_Salary.csv'); sl=sl[(sl.Mode=='All')&(sl.Skill_Group=='All')&(sl.Work_Population=='Paid employment is most important activity')][['UKPRN','Year','Salary_Band','Number']]
r=rd('Fact_Reflections.csv'); r=r[(r.Activity=='All')&(r.Domicile=='All')&(r.Interim==X)][['UKPRN','Year','Question','Answer','Percent']]
for n,d in [('Dash_Activity',a),('Dash_Occupation',o),('Dash_Subject',s),('Dash_Salary',sl),('Dash_Reflection',r)]: d.to_csv(D+n+'.csv',index=False)
for f in ['Dim_Provider','Dim_Year','Dim_Activity','Dim_SOC','Dim_Subject','Dim_SalaryBand','Dim_ReflectionQuestion','Dim_ReflectionAnswer']: shutil.copy(O+f+'.csv',D+f+'.csv')
W=['Full-time employment','Part-time employment','Unknown pattern of employment','Voluntary or unpaid work','Employment and further study']
S=['Full-time further study','Part-time further study','Unknown pattern of further study','Employment and further study']
def kp(df,by):
    p=df.pivot_table(index=by,columns='Activity',values='Number',aggfunc='sum').fillna(0)
    k=p['Total with known outcomes']
    return pd.DataFrame({'n':p['Total'],'k':k,'resp':k/p['Total'],'work':p[W].sum(axis=1)/k,'study':p[S].sum(axis=1)/k,'unemp':p['Unemployed']/k})
import os; Y=os.environ.get('LATEST_YEAR','2023/24')
tr=kp(a,'Year'); 
ho=o.pivot_table(index=['UKPRN','Year'],columns='SOC',values='Number',aggfunc='sum').fillna(0)
hsY=ho.groupby('Year').sum(); hsY=hsY['Total high skilled']/(hsY['Total']-hsY['Unknown'])
u=kp(a[a.Year==Y],'UKPRN'); hu=ho.xs(Y,level='Year'); u['hs']=hu['Total high skilled']/(hu['Total']-hu['Unknown'])
rf=r[(r.Year==Y)&(r.Question=='My current activity is meaningful')&r.Answer.isin(['Agree','Strongly agree'])].groupby('UKPRN').Percent.sum(); u['agree']=rf
am=a[(a.Year==Y)].groupby('Activity').Number.sum()
mix={k:int(am[k]) for k in am.index if k not in('Total','Total with known outcomes','Non-respondents')}
sj=s[s.Year==Y]; sp=sj.pivot_table(index='Subject',columns='Activity',values='Number',aggfunc='sum').fillna(0)
import re
sp=sp[sp.index.str.match(r'^\d\d ')]; sp['K']=sp[[c for c in sp.columns if c not in('Total','Total with known outcomes','Non-respondents')]].sum(axis=1); sp=sp[sp['K']>=1500]
sw=(sp[W].sum(axis=1)/sp['K']).sort_values(ascending=False)
sal=sl[(sl.Year==Y)].groupby('Salary_Band').Number.sum(); tot=sal.pop('Total')
bands=pd.read_csv(O+'Dim_SalaryBand.csv'); order=[b for b in bands.Salary_Band if b!='Total']
R=lambda x,d=4:round(float(x),d)
data={'year':Y,'n':int(tr.loc[Y,'n']),'k':int(tr.loc[Y,'k']),
 'trend':{'years':list(tr.index),'work':[R(x) for x in tr.work],'study':[R(x) for x in tr.study],'unemp':[R(x) for x in tr.unemp],'resp':[R(x) for x in tr.resp],'hs':[R(x) for x in hsY]},
 'rg':{'resp':R(tr.loc[Y,'resp']),'work':R(tr.loc[Y,'work']),'study':R(tr.loc[Y,'study']),'unemp':R(tr.loc[Y,'unemp']),'hs':R(hsY[Y]),'agree':R((u.agree*u.k).sum()/u.k[u.agree.notna()].sum())},
 'unis':[{'u':nm[i],'resp':R(r_.resp),'work':R(r_.work),'study':R(r_.study),'unemp':R(r_.unemp),'hs':R(r_.hs),'agree':R(r_.agree),'k':int(r_.k)} for i,r_ in u.iterrows()],
 'mix':mix,'subj':[[re.sub(r'^\d\d ','',k),R(v)] for k,v in sw.items()],
 'sal':[[b.replace('Less than ','<').replace(' - ','–'),R(sal[b]/tot)] for b in order],
 'subjk':{re.sub(r'^\d\d ','',k):int(v) for k,v in sp['K'].items()}}
json.dump(data,open('dash/data.json','w'),separators=(',',':'))
import os; print(os.path.getsize('dash/data.json'),len(data['subj']),data['rg'],data['sal'][:3])
