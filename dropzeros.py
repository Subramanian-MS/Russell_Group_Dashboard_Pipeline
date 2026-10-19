"""Removes zero-count rows from the large count tables (a missing row means zero)."""
import pandas as pd, os
for n in ['Fact_Subject','Fact_Activity_Sex','Fact_Activity_Age','Fact_Activity_Disability','Fact_Activity_Ethnicity','Fact_Industry','Fact_Occupation']:
    f=f'out/{n}.csv'; first=True
    for ch in pd.read_csv(f,dtype=str,chunksize=500000,keep_default_na=False):
        ch[ch.Number!='0'].to_csv(f+'.tmp',mode='w' if first else 'a',header=first,index=False); first=False
    os.replace(f+'.tmp',f)
