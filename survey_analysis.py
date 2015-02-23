import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
import statsmodels.api as sm
from tabulate import tabulate 

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
second = re.compile('Somewhat Agree',re.IGNORECASE)
third = re.compile('Not Sure',re.IGNORECASE)
fourth = re.compile('Somewhat Disagree',re.IGNORECASE)
fifth = re.compile('Strongly Disagree',re.IGNORECASE)

for column in ['Q12', 'Q13', 'Q14', 'Q16','Q18', 'Q20', 'Q21', 'Q23','Q27', 'Q28', 'PostQ30']:
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(first,1)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(second,2)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(third,3)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fourth,4)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fifth,5)

for column in ['Q15','Q17','Q19','Q22', 'Q24','Q25','Q26']:
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(first,5)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(second,4)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(third,3)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fourth,2)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fifth,1)

df = df.replace(' ',np.nan)
for column, series in df.iteritems():
    if not column in ['Name', 'Prison_ID', 'ID']:
        df[column] = df[column].astype('category')

attitudinal_scales_df = attitudinal_scales_df.replace('33',3)
attitudinal_scales_df = attitudinal_scales_df.replace(' ',np.nan)
for column, series in df.iteritems():
    if column in ['Prison','Gender', 'Group', 'Data_Round', 'Samples']:
        df[column] = df[column].astype('category')
    
#prison_count= df['Prison'].value_counts()
#prison_count.plot(kind = 'bar',title = 'Count of Prisons', color = ['r','b','g'] ,fontsize = 12)
#g = sns.factorplot('Prison', data=df , palette = 'Pastel1', legend= True,margin_titles = True)
#g.set_titles('Count of Prisons') # doesn't work

#for columns in attitudinal_scales_df.columns.values:
#    print [columns, attitudinal_scales_df[columns].value_counts(dropna=False)] #just checking distinct values of each var

#a = [('Time Management', ['Q12', 'Q17', 'Q22']),
#     ('Achievement Motivation', ...)]
#     
#attitudinal_scales_df['Time Management'] = attitudinal_scales_df[['Q12','Q17','Q22']].mean(axis=1,skipna=False)
#attitudinal_scales_df['Achievement Motivation'] = attitudinal_scales_df[['Q13','Q18']].mean(axis=1,skipna=False)
#attitudinal_scales_df['Intellectual Flexibility'] = attitudinal_scales_df[['Q14','Q19','Q24','Q26']].mean(axis=1,skipna=False)
#attitudinal_scales_df['Emotional Control'] = attitudinal_scales_df[['Q15','Q20']].mean(axis=1,skipna=False)
#attitudinal_scales_df['Self Confidence'] = attitudinal_scales_df[['Q21']].mean(axis=1,skipna=False)
#attitudinal_scales_df['Social Competence'] = attitudinal_scales_df[['Q23','Q25','Q27','Q28']].mean(axis=1,skipna=False)


attitudinal_scales_df['Time Management'] = attitudinal_scales_df[['Q12','Q17','Q22']].sum(axis=1,skipna=False)
attitudinal_scales_df['Achievement Motivation'] = attitudinal_scales_df[['Q13','Q18']].sum(axis=1,skipna=False)
attitudinal_scales_df['Intellectual Flexibility'] = attitudinal_scales_df[['Q14','Q19','Q24','Q26']].sum(axis=1,skipna=False)
attitudinal_scales_df['Emotional Control'] = attitudinal_scales_df[['Q15','Q20']].sum(axis=1,skipna=False)
attitudinal_scales_df['Self Confidence'] = attitudinal_scales_df[['Q21']].sum(axis=1,skipna=False)
attitudinal_scales_df['Social Competence'] = attitudinal_scales_df[['Q23','Q25','Q27','Q28']].sum(axis=1,skipna=False)

#print attitudinal_scales_df[[ 'Time Management', 'Achievement Motivation', 'Intellectual Flexibility' ,'Emotional Control','Self Confidence' ,'Social Competence']].describe()

pre_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Pre Program']
post_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Post-Program']

def hist():
    pre_df[[ 'Time Management', 'Achievement Motivation', 'Intellectual Flexibility' ,'Emotional Control','Self Confidence' ,'Social Competence']].hist()
    plt.suptitle("Pre-Program")
    
    post_df[[ 'Time Management', 'Achievement Motivation', 'Intellectual Flexibility' ,'Emotional Control','Self Confidence' ,'Social Competence']].hist()
    plt.suptitle("Post-Program")   
    plt.show()

def qqplot():
    return sm.qqplot(post_df['Time Management'],line = '45')
    
post_df = post_df[[ 'Time Management', 'Achievement Motivation', 'Intellectual Flexibility' , 'Emotional Control','Self Confidence' ,'Social Competence']].dropna()
pre_df = pre_df[[ 'Time Management', 'Achievement Motivation', 'Intellectual Flexibility' , 'Emotional Control','Self Confidence' ,'Social Competence']].dropna()

#print qqplot()
#plt.show()

#scipy.stats.shapiro(post_df['Time Management'])

for column in ['Time Management' , 'Achievement Motivation', 
                'Intellectual Flexibility' ,'Emotional Control',
                'Self Confidence' ,'Social Competence']:
     print 'post-program', column, sp.stats.shapiro(post_df[column])

post_table = [["Time Management", 0.7989435195922852, 1.7665534833566365e-12],
              ["Intellectual Flexibility", 0.8067236542701721, 3.310084845109529e-12],
         ["Achievement Motivation" ,0.5009009838104248, 1.0594767746240141e-19],
         ["Emotional Control", 0.8851432800292969, 6.317574907654944e-09],
         ["Self Confidence", 0.609407901763916, 1.4120606676629398e-17],
        ["Social Competence", 0.8981918692588806, 3.001261816848455e-08]]
post = tabulate(post_table,headers = ["Attribute", "W stat", "p value"], floatfmt = ".2f", tablefmt = 'rst')

file1 = open("tables.txt",'w')
file1.write('Post-Program - Shapiro Wilk test for normality\n')
file1.write(post)
file1.close()