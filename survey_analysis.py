import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels as sms
from tabulate import tabulate 
import re
import patsy

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

df = df[['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'PreQ1','PreQ2a', 'PreQ2b', 'PreQ2c', 'PreQ2d', 'PreQ2e', 'PreQ3a',
       'PreQ3b', 'PreQ3c', 'PreQ3d', 'PreQ3e', 'PreQ3f', 'PreQ3g','PreQ3h', 'PreQ4', 'PreQ5a', 'PreQ5b', 'PreQ5c', 'PreQ5d', 'PreQ6',
       'PreQ7', 'PreQ8', 'PreQ9a', 'PreQ9b', 'PReQ9c', 'PreQ9d', 'PreQ9e','PreQ10a', 'PreQ10b', 'PreQ10c', 'PreQ10d', 'PreQ10e', 'PreQ10f',
       'PreQ11a', 'PreQ11b', 'PreQ11c', 'PreQ11d', 'PreQ11e', 'PreQ11f','PreQ11g', 'PreQ11h', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28', 'PostQ30','PostQ1', 'PostQ2a', 'PostQ2b', 'PostQ2c', 'PostQ2d',
       'PostQ2e', 'PostQ3a', 'PostQ3b', 'PostQ3c', 'PostQ3d', 'PostQ3e','PostQ3f', 'PostQ3g', 'PostQ3h', 'PostQ4', 'PostQ5a', 'PostQ5b',
       'PostQ5c', 'PostQ5d', 'PostQ6', 'PostQ7', 'PostQ8a', 'PostQ8b','PostQ8c', 'PostQ8d', 'PostQ8e', 'PostQ8f', 'PostQ8g', 'PostQ8h',
       'PostQ8i', 'PostQ8j', 'PostQ9', 'PostQ10a', 'PostQ10b', 'PostQ10c','PostQ10d', 'PostQ10e', 'PostQ11a', 'PostQ11b', 'PostQ11c',
       'PostQ11d', 'PostQ12a', 'PostQ12b', 'PostQ12c', 'PostQ12d','PostQ12e', 'PostQ12f', 'PostQ12g', 'PostQ12h']]
       
columns_to_keep = ['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'PreQ1', 'PostQ1','Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28', 'PostQ30']
attitudinal_scales_df = pd.DataFrame(df,columns = columns_to_keep)

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

#creating a column for previous art experience
attitudinal_scales_df['art_experience'] = attitudinal_scales_df['PostQ1']
for index, values in attitudinal_scales_df['PreQ1'].iteritems():
    if values in ['Yes, both studied and practiced', 'Yes, practiced', 'Yes, studied' ]:
        attitudinal_scales_df.loc[index, 'art_experience'] = 'Yes'
        
    elif values == "No, I haven't":
        attitudinal_scales_df.loc[index, 'art_experience'] ='No'    

for column,questions in [('Time Management',['Q12','Q17','Q22']),
                ('Achievement Motivation',['Q13','Q18','Q16' ]),
                ('Intellectual Flexibility',['Q14','Q19','Q24','Q26']),
                ('Emotional Control',['Q15','Q20']),
                ('Self Confidence',['Q21']),
                ('Social Competence', ['Q23','Q25','Q27','Q28'])]:
    
    attitudinal_scales_df[column] = attitudinal_scales_df[questions].mean(axis=1,skipna=False)
    
attributes =  ['Time Management', 'Achievement Motivation', 'Intellectual Flexibility' , 'Emotional Control','Self Confidence' ,'Social Competence']
pre_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Pre Program']
post_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Post-Program']

columns_atscales = ['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples','art_experience','Time Management',
 'Achievement Motivation', 'Intellectual Flexibility', 'Emotional Control',
 'Self Confidence', 'Social Competence']

pre_df = pd.DataFrame(pre_df, columns = columns_atscales)
post_df = pd.DataFrame(post_df, columns = columns_atscales)

def hist():
    post = post_df[attributes].dropna()
    pre=  pre_df[attributes].dropna()
    pre[attributes].hist()
    plt.suptitle("Pre-Program")
    
    post[attributes].hist()
    plt.suptitle("Post-Program")   
    plt.show()

def qqplot():
    return sm.qqplot(post_df['Time Management'],line = '45')
    
def test_normality():
    #for column in attributes:
    #     print column, sp.stats.shapiro(post_df[column])
    
    post_table = [["Time Management", 0.7989435195922852, 1.7665534833566365e-12],
                  ["Intellectual Flexibility", 0.8067236542701721, 3.310084845109529e-12],
                  ["Achievement Motivation" ,0.5009009838104248, 1.0594767746240141e-19],
                  ["Emotional Control", 0.8851432800292969, 6.317574907654944e-09],
                  ["Self Confidence", 0.609407901763916, 1.4120606676629398e-17],
                  ["Social Competence", 0.8981918692588806, 3.001261816848455e-08]]
    post = tabulate(post_table,headers = ["Attribute", "W stat", "p value"], floatfmt = ".2f", tablefmt = 'rst')

    #for column in attributes:
    #    print column, sp.stats.shapiro(pre_df[column])
    
    pre_table = [["Time Management", 0.9098374843597412, 8.103528159608686e-08],
                 ["Intellectual Flexibility", 0.9260804057121277, 8.383431122638285e-07],
                 ["Achievement Motivation" ,0.7117029428482056, 1.8042233763319697e-15],
                 ["Emotional Control", 0.9423717856407166, 1.190870170830749e-05,],
                 ["Self Confidence", 0.7873598337173462, 3.5050795274028934e-13],
                 ["Social Competence", 0.9072498083114624, 5.7175618906057935e-08]]

    pre = tabulate(pre_table,headers = ["Attribute", "W stat", "p value"], floatfmt = ".2f", tablefmt = 'rst')

    return (post, pre)

file1 = open("tables.txt",'w')
file1.write('Shapiro Wilk Test For Normality (Pre-Program)\n')
file1.write(test_normality()[1] + '\n' + 'W stat is significant for all attributes, therefore we can reject the null that the data comes from a normal distribution.\n\n')
file1.write('Shapiro Wilk Test For Normality (Post-Program)\n')
file1.write(test_normality()[0] + '\n' + 'W stat is significant for all attributes, therefore we can reject the null that the data comes from a normal distribution.\n\n\n\n')

#Data is not normal, therefore running non parametric tests. 

# Descriptive stats

def descriptive_stats():
    pre = pre_df[attributes].describe() 
    post = post_df[attributes].describe()
    pre = tabulate(pre,headers = attributes,
                    tablefmt = 'rst', floatfmt = '.2f')
    post = tabulate(post, headers = attributes,
                    tablefmt = 'rst', floatfmt = '.2f')
    return (pre,post)
    
file1.write('Descriptive Statistics (Pre-Program)\n')
file1.write(descriptive_stats()[0] +'\n\n')
file1.write('Descriptive Statistics (Post-Program)\n')
file1.write(descriptive_stats()[1] + '\n\n\n\n')


def mannwhitney(Samples = 'Independent'):
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Samples != 'Independent':
        pre_noart = pre_noart.loc[pre_noart['Samples'] == 'Paired']
        pre_art = pre_art.loc[pre_art['Samples'] == 'Paired']
        post_noart= post_noart.loc[post_noart['Samples'] =='Paired']
        post_art= post_art.loc[post_art['Samples'] == 'Paired']
    
    table_noart = []
    for column in attributes:
        u_noart, p_noart = sp.stats.mannwhitneyu(pre_noart[column],post_noart[column], use_continuity = False) 
        #print pre_noart['art_experience'].value_counts(), column, (u_noart,round(p_noart,4)) 
        table_noart.append([column, u_noart, round(p_noart,4)])
        
    table_art = []
    for column in attributes:
        u_art, p_art = sp.stats.mannwhitneyu(pre_art[column],post_art[column], use_continuity = False) 
        #print pre_art['art_experience'].value_counts(), column, (u_art,round(p_art,4)) 
        table_art.append([column, u_art, round(p_art,4)])

    return (tabulate(table_noart, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'))

file1.write('Mann Whitney U test - Without Art Experience(Whole Sample)\n')
file1.write(mannwhitney()[0] +'\n\n\n\n')
file1.write('Mann Whitney U test - With Art Experience(Whole Sample)\n')
file1.write(mannwhitney()[1] + '\n\n\n\n')


def wilcoxon():
    ''' Signed Wilcoxon ranked test, only for paired samples
    '''   
    #pre = pre_df.loc[pre_df['Samples'] == 'Paired']
    #post = post_df.loc[post_df['Samples'] == 'Paired']
    
    pre = pre_df.loc[pre_df['Gender'] == 'Female']
    post = post_df.loc[post_df['Gender'] == 'Female']
    
    for column in attributes:        
        #diff = np.subtract(post[column], pre[column])
        t,p = sp.stats.wilcoxon(pre[column], post[column])
        print column, t, round(p,4)
        

def ranksums(Samples = 'Independent'):
    '''Wilcoxon for independent samples, like mann whitney
    '''
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Samples != 'Independent':
        pre_noart = pre_noart.loc[pre_noart['Samples'] == 'Paired']
        pre_art = pre_art.loc[pre_art['Samples'] == 'Paired']
        post_noart= post_noart.loc[post_noart['Samples'] =='Paired']
        post_art= post_art.loc[post_art['Samples'] == 'Paired']
    
    table_noart = []
    for column in attributes:
        z_noart, p_noart = sp.stats.ranksums(pre_noart[column],post_noart[column])
        table_noart.append([column, z_noart, round(p_noart,4)]) 
    
    table_art = []    
    for column in attributes:
        z_art, p_art = sp.stats.ranksums(pre_art[column],post_art[column])  
        table_art.append([column, z_art, round(p_art,4)]) 
    
    return (tabulate(table_noart, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'))

file1.write('Wilcoxon Rank Sums Test - Without Art Experience(Whole Sample)\n')
file1.write(ranksums()[0] +'\n\n\n\n')
file1.write('Wilcoxon Rank Sums Test - With Art Experience(Whole Sample)\n')
file1.write(ranksums()[1] + '\n\n\n\n')


def stats_artexp():
    pre_stats = pre_df.groupby('art_experience')
    pre_table = []
    for column in attributes:
        pre_table.append([column, pre_stats[column].agg([np.count_nonzero, np.mean, np.std])])
    post_stats = post_df.groupby('art_experience')
    post_table = []
    for column in attributes:
        post_table.append([column, post_stats[column].agg([np.count_nonzero,np.mean, np.std])])

    return (tabulate(pre_table, tablefmt = 'rst', floatfmt = '.4f', numalign = 'right'),
            tabulate(post_table, tablefmt = 'rst', floatfmt = '.4f', numalign = 'right'))

file1.write('Descriptive statistics - Without Art Experience(Whole Sample)\n')
file1.write(stats_artexp()[0] +'\n\n\n\n')
file1.write('Descriptive statistics - With Art Experience(Whole Sample)\n')
file1.write(stats_artexp()[1] + '\n\n\n\n')

def ttest_ind(Gender = 'all'):
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Gender == 'Male':
        pre_noart = pre_noart.loc[pre_noart['Gender'] == 'Male']
        pre_art = pre_art.loc[pre_art['Gender'] == 'Male']
        post_noart= post_noart.loc[post_noart['Gender'] == 'Male']
        post_art= post_art.loc[post_art['Gender'] == 'Male']
    
    table_noart = []
    for column in attributes:
        t_noart, p_noart = sp.stats.ttest_ind(pre_noart[column].dropna(),post_noart[column].dropna(),equal_var=False) 
        table_noart.append([column, t_noart, p_noart])
 
    table_art = []   
    for column in attributes:
        t_art, p_art = sp.stats.ttest_ind(pre_art[column].dropna(),post_art[column].dropna(),equal_var=False)
        table_art.append([column, t_art, p_art])

    return (tabulate(table_noart, headers = ['Attribute','t stat', 'p value'], tablefmt = "pipe", floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','t stat', 'p value'], tablefmt = "pipe", floatfmt = '.4f'))
        
file1.write('Independent Samples t-test - Without Art Experience(Whole Sample)\n')
file1.write(ttest_ind()[0] +'\n\n\n\n')
file1.write('Independent Samples t-test - With Art Experience(Whole Sample)\n')
file1.write(ttest_ind()[1] + '\n\n\n\n')
file1.close()


#altered for females(for pairing)

def ttest_paired(Gender='Female'):
    pre_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Pre Program']
    post_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Post-Program']
    pre = pre_df.loc[pre_df['Gender'] == Gender]
    post = post_df.loc[post_df['Gender'] == Gender]
    
    #replacing missing values with 3(neutral score)
    
    for column in ['Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28',]:
        pre[column] = pre[column].replace(np.nan,3)
        post[column] = post[column].replace(np.nan,3)
    
    for attribute,questions in [('Time Management',['Q12','Q17','Q22']),
                ('Achievement Motivation',['Q13','Q18','Q16' ]),
                ('Intellectual Flexibility',['Q14','Q19','Q24','Q26']),
                ('Emotional Control',['Q15','Q20']),
                ('Self Confidence',['Q21']),
                ('Social Competence', ['Q23','Q25','Q27','Q28'])]:
    
        pre[attribute] = pre[questions].sum(axis=1,skipna=False)
        post[attribute] = post[questions].sum(axis=1,skipna=False)
        

    for column in attributes:
        t, p = sp.stats.ttest_rel(pre[column], post[column]) 
        print column, t, round(p,4)


#
#def pivot():
#    

print attitudinal_scales_df.columns





#prison_count= df['Prison'].value_counts()
#prison_count.plot(kind = 'bar',title = 'Count of Prisons', color = ['r','b','g'] ,fontsize = 12)
#g = sns.factorplot('Prison', data=df , palette = 'Pastel1', legend= True,margin_titles = True)
#g.set_titles('Count of Prisons') # doesn't work
#     
#print df2['PostQ1']
#
#pre_df['Time Management'] = pre_df['Time Management'].dropna()
#print post_df.columns.values
#print pre_df.columns.values
#print pre_df




