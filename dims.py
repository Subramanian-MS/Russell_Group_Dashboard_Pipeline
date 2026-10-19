import os, pandas as pd, numpy as np, re, glob
OUT='out'
def uniq(f,col):
    s=set()
    for ch in pd.read_csv(f'{OUT}/{f}.csv',usecols=[col],dtype=str,chunksize=500000,keep_default_na=False): s|=set(ch[col].unique())
    return s
# Provider
short={'10006840':'Birmingham','10007786':'Bristol','10007788':'Cambridge','10007814':'Cardiff','10007143':'Durham','10007790':'Edinburgh','10007792':'Exeter','10007794':'Glasgow','10003270':'Imperial College London','10003645':"King's College London",'10007795':'Leeds','10006842':'Liverpool','10004063':'LSE','10007798':'Manchester','10007799':'Newcastle','10007154':'Nottingham','10007774':'Oxford','10007775':'Queen Mary London','10005343':"Queen's Belfast",'10007157':'Sheffield','10007158':'Southampton','10007784':'UCL','10007163':'Warwick','10007167':'York','10042500':'Global Banking School'}
raw=pd.read_csv('flt/table-1-'+os.environ.get('LATEST_YEAR','2023/24').replace('/','-')+'.csv',dtype=str,usecols=['UKPRN','Provider name','Country of provider'])
ctry=raw[raw['Country of provider']!='All'].drop_duplicates('UKPRN').set_index('UKPRN')['Country of provider']
full=raw.drop_duplicates('UKPRN').set_index('UKPRN')['Provider name']
p=pd.DataFrame({'UKPRN':list(short)})
p['Provider']=p.UKPRN.map(short); p['Provider_Full_Name']=p.UKPRN.map(full); p['Country']=p.UKPRN.map(ctry)
p['Group']=np.where(p.UKPRN=='10042500','GBS (reference)','Russell Group')
p['Is_GBS']=(p.UKPRN=='10042500').astype(int)
p['Provider_Sort']=range(1,len(p)+1)
p.to_csv(f'{OUT}/Dim_Provider.csv',index=False)
# Year
yrs=sorted(uniq('Fact_Activity_CI','Year'))
pd.DataFrame({'Year':yrs,'Year_Sort':range(1,len(yrs)+1),'Graduation_Year':[int(y[:4])+1 for y in yrs],'Is_Latest':[int(y==yrs[-1]) for y in yrs]}).to_csv(f'{OUT}/Dim_Year.csv',index=False)
# Activity
act=[('Full-time employment','Employment','Outcome'),('Part-time employment','Employment','Outcome'),('Unknown pattern of employment','Employment','Outcome'),('Voluntary or unpaid work','Employment','Outcome'),('Employment and further study','Employment and further study','Outcome'),('Full-time further study','Further study','Outcome'),('Part-time further study','Further study','Outcome'),('Unknown pattern of further study','Further study','Outcome'),('Other including travel, caring for someone or retired','Other','Outcome'),('Unemployed','Unemployed','Outcome'),('Total with known outcomes','Total','Total with known outcomes (respondents)'),('Non-respondents','Total','Non-respondents'),('Total','Total','Total graduate population')]
a=pd.DataFrame(act,columns=['Activity','Activity_Group','Row_Type']); a['Activity_Sort']=range(1,len(a)+1)
a['Is_Outcome_Category']=(a.Row_Type=='Outcome').astype(int)
a.to_csv(f'{OUT}/Dim_Activity.csv',index=False)
# simple dims
def simple(name,col,vals,order=None):
    vals=sorted(vals,key=lambda v:(order.index(v) if order and v in order else 99,v))
    pd.DataFrame({col:vals,col+'_Sort':range(1,len(vals)+1)}).to_csv(f'{OUT}/{name}.csv',index=False)
simple('Dim_Level','Level',uniq('Fact_Activity_Sex','Level'),['All','Undergraduate','Postgraduate'])
simple('Dim_Mode','Mode',uniq('Fact_Activity_Sex','Mode'),['All','Full-time','Part-time','Not applicable or not known'])
simple('Dim_Domicile','Domicile',uniq('Fact_Activity_Sex','Domicile'),['All','UK','Non-UK','Not known'])
simple('Dim_Interim','Interim',uniq('Fact_Activity_Sex','Interim'),['Exclude significant interim study','Include significant interim study'])
simple('Dim_Sex','Sex',uniq('Fact_Activity_Sex','Sex'),['All','Female','Male','Unknown'])
simple('Dim_Age','Age_Group',uniq('Fact_Activity_Age','Age_Group'),['All','20 and under','21-24 years','25-29 years','30 years and over','Age unknown'])
simple('Dim_Disability','Disability',uniq('Fact_Activity_Disability','Disability'),['All','Known disability','No known disability'])
simple('Dim_Ethnicity','Ethnicity',uniq('Fact_Activity_Ethnicity','Ethnicity'),['All','Asian','Black','Mixed','Other','White','Not known'])
simple('Dim_WorkType','Work_Type',uniq('Fact_Industry','Work_Type'),['All','Paid employment','Self-employed, own business or portfolio','Volunteer work'])
# SOC
soc=uniq('Fact_Occupation','SOC')
sm={'Managers, directors and senior officials':('High skilled','Major group',1),'Professional occupations':('High skilled','Major group',2),'Associate professional occupations':('High skilled','Major group',3),'Total high skilled':('High skilled','Subtotal',4),'Administrative and secretarial occupations':('Medium skilled','Major group',5),'Skilled trades occupations':('Medium skilled','Major group',6),'Caring, leisure and other service occupations':('Medium skilled','Major group',7),'Total medium skilled':('Medium skilled','Subtotal',8),'Sales and customer service occupations':('Low skilled','Major group',9),'Process, plant and machine operatives':('Low skilled','Major group',10),'Elementary occupations':('Low skilled','Major group',11),'Total low skilled':('Low skilled','Subtotal',12),'Unknown':('Unknown','Unknown',13),'Total':('Total','Total',14)}
assert soc<=set(sm),soc-set(sm)
pd.DataFrame([(k,)+v for k,v in sm.items()],columns=['SOC','Skill_Level','Row_Type','SOC_Sort']).to_csv(f'{OUT}/Dim_SOC.csv',index=False)
# SIC
sic=sorted(uniq('Fact_Industry','SIC'))
rows=[(s,'Total' if s=='Total' else ('Unknown' if s=='Unknown' else 'Section')) for s in sic]
d=pd.DataFrame(rows,columns=['SIC','Row_Type']); d['_o']=d.Row_Type.map({'Section':0,'Unknown':1,'Total':2}); d=d.sort_values(['_o','SIC']).drop(columns='_o'); d['SIC_Sort']=range(1,len(d)+1)
d.to_csv(f'{OUT}/Dim_SIC.csv',index=False)
# Subject
sub=sorted(uniq('Fact_Subject','Subject'))
rows=[]
for s in sub:
    m=re.match(r'^(\d{2}) (.*)$',s)
    if m: rows.append((s,m.group(1),m.group(2),'Subject'))
    else: rows.append((s,'',s,'Total' if s=='Total' else ('Unknown' if s.startswith('Unknown') else 'Subtotal')))
d=pd.DataFrame(rows,columns=['Subject','CAH_Code','Subject_Name','Row_Type']); d['_o']=d.Row_Type.map({'Subject':0,'Unknown':1,'Subtotal':2,'Total':3}); d=d.sort_values(['_o','Subject']).drop(columns='_o'); d['Subject_Sort']=range(1,len(d)+1)
d.to_csv(f'{OUT}/Dim_Subject.csv',index=False)
# Salary band
bands=[('Less than £15,000',0,14999)]+[(f'£{l:,} - £{l+2999:,}',l,l+2999) for l in range(15000,51000,3000)]+[('£51,000+',51000,np.nan),('Total',np.nan,np.nan)]
sb=pd.DataFrame(bands,columns=['Salary_Band','Band_Lower','Band_Upper']); sb['Band_Sort']=range(1,len(sb)+1); sb['Row_Type']=np.where(sb.Salary_Band=='Total','Total','Band')
fs=uniq('Fact_Salary','Salary_Band'); assert fs==set(sb.Salary_Band),(fs^set(sb.Salary_Band))
sb.to_csv(f'{OUT}/Dim_SalaryBand.csv',index=False)
# Reflection
q=uniq('Fact_Reflections','Question'); a_=['Strongly disagree','Disagree','Neither agree nor disagree','Agree','Strongly agree']
assert uniq('Fact_Reflections','Answer')==set(a_)
pd.DataFrame({'Question':sorted(q)}).assign(Question_Short=lambda x:x.Question.map({'My current activity is meaningful':'Meaningful','My current activity fits with my future plans':'Fits future plans','I am utilising what I learnt during my studies in my current activity':'Using what I learnt'}),Question_Sort=lambda x:range(1,len(x)+1)).to_csv(f'{OUT}/Dim_ReflectionQuestion.csv',index=False)
pd.DataFrame({'Answer':a_,'Answer_Sort':range(1,6),'Is_Agree':[0,0,0,1,1]}).to_csv(f'{OUT}/Dim_ReflectionAnswer.csv',index=False)
print(p.to_string())
