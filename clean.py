import pandas as pd, numpy as np, glob, sys, os, re
OUT='out'
def rd(t):
    for f in sorted(glob.glob(f'flt/table-{t}-*.csv')):
        d=pd.read_csv(f,dtype=str,keep_default_na=False,na_values=[''])
        for c in d.columns:
            d[c]=d[c].str.replace('\xa0',' ',regex=False).str.strip()
        yield d
def pct(s): return pd.to_numeric(s.str.rstrip('%'),errors='coerce')/100
def write(df,name,first):
    df.to_csv(f'{OUT}/{name}.csv',mode='w' if first else 'a',header=first,index=False,encoding='utf-8')
REN={'Academic year':'Year','Permanent address':'Domicile','Level of qualification obtained':'Level','Mode of former study':'Mode','Interim study':'Interim'}
def base(d):
    if 'Country of provider' in d.columns:
        d=d[d['Country of provider']=='All'].drop(columns=['Country of provider'])
    d=d.drop(columns=['Provider name'])
    return d.rename(columns=REN)
t=sys.argv[1]
spec={'1':('Fact_Activity_Sex',['UKPRN','Year','Domicile','Level','Mode','Interim','Sex','Activity']),
 '2':('Fact_Activity_Age',['UKPRN','Year','Domicile','Level','Mode','Interim','Age group','Activity']),
 '3':('Fact_Activity_Disability',['UKPRN','Year','Domicile','Level','Mode','Interim','Disability','Activity']),
 '4':('Fact_Activity_Ethnicity',['UKPRN','Year','Level','Mode','Interim','Ethnicity','Activity']),
 '19':('Fact_Industry',['UKPRN','Year','Domicile','Work type marker','Level','Mode','Standard industrial classification']),
 '22':('Fact_Occupation',['UKPRN','Year','Domicile','Work type marker','Level','Mode','Standard occupational classification']),
 '28':('Fact_Subject',['UKPRN','Year','Level','Mode','Interim','Subject area of degree','Activity'])}
first=True
if t in spec:
    name,cols=spec[t]
    for d in rd(t):
        d=base(d)
        d['Number']=pd.to_numeric(d['Number']).astype('int32')
        d=d.rename(columns={'Age group':'Age_Group','Work type marker':'Work_Type','Standard industrial classification':'SIC','Standard occupational classification':'SOC','Subject area of degree':'Subject'})
        write(d,name,first); first=False
elif t=='6':
    for d in rd('6'):
        d=base(d)
        d['Number']=pd.to_numeric(d['Number']).astype('int32')
        d['Percent']=pct(d['Percent'])
        ci=d['95% confidence interval'].str.extract(r'\((\d+)%-(\d+)%\)').astype(float)/100
        d['CI_Low']=ci[0]; d['CI_High']=ci[1]
        d=d.drop(columns=['95% confidence interval'])
        write(d,'Fact_Activity_CI',first); first=False
elif t=='5':
    for d in rd('5'):
        d=d[(d['Country of provider']=='All')&(d['Provider type']=='All')].drop(columns=['Country of provider','Provider name','Provider type'])
        d=d.rename(columns={'Academic year':'Year','Permanent address':'Domicile_Detail','Level of qualification obtained':'Level_Detail'})
        d['Value']=np.where(d.Category=='Total graduate population',pd.to_numeric(d.Value,errors='coerce'),pct(d.Value))
        w=d.pivot_table(index=['UKPRN','Year','Domicile_Detail','Level_Detail'],columns='Category',values='Value',aggfunc='first').reset_index()
        w=w.rename(columns={'Survey completed response rate':'Completed_Rate','Survey partial response rate':'Partial_Rate','Survey (complete + partial) response rate':'Response_Rate','Total graduate population':'Graduate_Population'})
        w.columns.name=None
        write(w,'Fact_ResponseRate',first); first=False
elif t=='8':
    for d in rd('8'):
        d=base(d)
        d['Percent']=pct(d['Percent'])
        d=d.rename(columns={'Graduate reflection question':'Question','Answer grouping':'Answer'})
        write(d,'Fact_Reflections',first); first=False
elif t=='26':
    for d in rd('26'):
        d=d[d['Country of provider']=='All'].drop(columns=['Country of provider','Provider name'])
        d=d.rename(columns={'Academic year':'Year','Mode of former study':'Mode','Skill group':'Skill_Group','Work population marker':'Work_Population','Salary band':'Salary_Band'})
        d['Number']=pd.to_numeric(d['Number']).astype('int32'); d['Percent']=pct(d['Percent'])
        write(d,'Fact_Salary',first); first=False
print('done',t)
