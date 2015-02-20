import numpy as np
import pandas as pd
import seaborn as sns

df1 = pd.read_csv('/Users/kritikarai/Desktop/PrisonData/PrisonData_2015_1.csv')
df1 = df1.drop('ID_Check',axis=1)
df1 = df1.iloc[:144]
df2 = pd.read_csv('/Users/kritikarai/Desktop/PrisonData/PrisonData_2014.csv')
df = pd.concat([df1,df2] ,join = 'outer', ignore_index = True)

new = open('/Users/kritikarai/Desktop/finaldata.csv','w')
df.to_csv(new)
new.close()

columns_drop = ['AM','EC','IF','S0','SC','TM','NewPreQ1','NewQ15','NewQ17','NewQ19','NewQ22','NewQ24','NewQ25','NewQ26','filter_$']
df = df.drop(columns_drop,axis =1)

cols = df1.columns.values

df = df[['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'PreQ1',
       'PreQ2a', 'PreQ2b', 'PreQ2c', 'PreQ2d', 'PreQ2e', 'PreQ3a',
       'PreQ3b', 'PreQ3c', 'PreQ3d', 'PreQ3e', 'PreQ3f', 'PreQ3g',
       'PreQ3h', 'PreQ4', 'PreQ5a', 'PreQ5b', 'PreQ5c', 'PreQ5d', 'PreQ6',
       'PreQ7', 'PreQ8', 'PreQ9a', 'PreQ9b', 'PReQ9c', 'PreQ9d', 'PreQ9e',
       'PreQ10a', 'PreQ10b', 'PreQ10c', 'PreQ10d', 'PreQ10e', 'PreQ10f',
       'PreQ11a', 'PreQ11b', 'PreQ11c', 'PreQ11d', 'PreQ11e', 'PreQ11f',
       'PreQ11g', 'PreQ11h', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26',
       'Q27', 'Q28', 'PostQ30','PostQ1', 'PostQ2a', 'PostQ2b', 'PostQ2c', 'PostQ2d',
       'PostQ2e', 'PostQ3a', 'PostQ3b', 'PostQ3c', 'PostQ3d', 'PostQ3e',
       'PostQ3f', 'PostQ3g', 'PostQ3h', 'PostQ4', 'PostQ5a', 'PostQ5b',
       'PostQ5c', 'PostQ5d', 'PostQ6', 'PostQ7', 'PostQ8a', 'PostQ8b',
       'PostQ8c', 'PostQ8d', 'PostQ8e', 'PostQ8f', 'PostQ8g', 'PostQ8h',
       'PostQ8i', 'PostQ8j', 'PostQ9', 'PostQ10a', 'PostQ10b', 'PostQ10c',
       'PostQ10d', 'PostQ10e', 'PostQ11a', 'PostQ11b', 'PostQ11c',
       'PostQ11d', 'PostQ12a', 'PostQ12b', 'PostQ12c', 'PostQ12d',
       'PostQ12e', 'PostQ12f', 'PostQ12g', 'PostQ12h']]
       
columns_to_keep = ['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28', 'PostQ30']
attitudinal_scales_df = pd.DataFrame(df,columns = columns_to_keep)
attitudinal_scales_df.tail(5) 

import re
first = re.compile('Strongly Agree',re.IGNORECASE)
attitudinal_scales_df = attitudinal_scales_df.replace(first,1)
second = re.compile('Somewhat Agree',re.IGNORECASE)
attitudinal_scales_df = attitudinal_scales_df.replace(second,1)
third = re.compile('Not Sure',re.IGNORECASE)
attitudinal_scales_df = attitudinal_scales_df.replace(third,1)
fourth = re.compile('Somewhat Disagree',re.IGNORECASE)
attitudinal_scales_df = attitudinal_scales_df.replace(fourth,4)
fifth = re.compile('Strongly Disagree',re.IGNORECASE)
attitudinal_scales_df = attitudinal_scales_df.replace(fifth,5)

print 'Q12', attitudinal_scales_df['Q12'].value_counts()
print 'Q13', attitudinal_scales_df['Q13'].value_counts()
print 'Q14', attitudinal_scales_df['Q14'].value_counts()
print 'Q15', attitudinal_scales_df['Q15'].value_counts()
print 'Q16', attitudinal_scales_df['Q16'].value_counts()

df = df.replace(' ',np.nan)
for column, series in df.iteritems():
    if not column in ['Name', 'Prison_ID', 'ID']:
        df[column] = df[column].astype('category')

attitudinal_scales_df = attitudinal_scales_df.replace(' ',np.nan)
for column, series in df.iteritems():
    if column in ['Prison','Gender', 'Group', 'Data_Round', 'Samples']:
        df[column] = df[column].astype('category')

prison_count= df['Prison'].value_counts()
prison_count.plot(kind = 'bar',title = 'Count of Prisons', color = ['r','b','g'] ,fontsize = 12)
g = sns.factorplot('Prison', data=df , palette = 'Pastel1', legend= True,margin_titles = True)
g.set_titles('Count of Prisons') # doesn't work
#
#attitudinal_scales_df['Q12'].value_counts(dropna=False)
#
#for columns in attitudinal_scales_df.columns.values: 
#    attitudinal_scales_df[columns] = attitudinal_scales_df[columns].str.lower()
#print attitudinal_scales_df


