# Pre-processing

#%%
import pandas as pd
import numpy as np
import pyreadstat

# ISCO code scheme
# Source: International Labour Organization (ISCO) 
# URL: https://www.ilo.org/ilostat-files/Documents/ISCO.xlsx
#%%
isco = pd.read_excel('ISCO.xlsx', sheet_name = 'ISCO_08', dtype = str,
                     usecols=['unit','description'])
isco['isco'] = isco['unit'] + ' ' + isco['description']
isco['unit'] = isco['unit'].astype('int')
isco = isco[['unit', 'isco']]
isco.head()

# ISIC code scheme
# Source: International Labour Organization (ISCO) 
# # URL: http://www.ilo.org/ilostat-files/Documents/ISIC.xlsx
#%%
isic = pd.read_excel('ISIC.xlsx', sheet_name = 'ISIC_Rev_4', dtype = str,
                     usecols=['4-digits ','description'])
isic['isic'] = isic['4-digits '] + ' ' + isic['description']
isic['4-digits '] = np.where(isic['4-digits '].str.len() == 3, isic['4-digits '].str.zfill(4), isic['4-digits '])
isic = isic[['4-digits ', 'isic']]
isic.head()

# Nigeria Labour Force Survey Q1 2024
# Source: https://microdata.nigerianstat.gov.ng/index.php/catalog/151
#%%
q1_raw, meta = pyreadstat.read_dta('NLFS_2024Q1_INDIVIDUAL 1.dta',
                                encoding='utf-8',
                                usecols=['interview_key','mjj1','mjj2a','mjj2b','mjj2cclean','sjj1a','sjj1b','sjj1cclean',
                                         'mjj3a','mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean'])
# ISCO main
isco_q1_main = pd.merge(q1_raw, isco, left_on='mjj2cclean', right_on='unit', how='left')
isco_q1_main = isco_q1_main[isco_q1_main['mjj1'].notnull()]
isco_q1_main = isco_q1_main.rename(columns={'mjj1':'jobnumber',
                                            'mjj2a':'occupationname',
                                            'mjj2b':'occupationtasksduties'})
isco_q1_main = isco_q1_main[['interview_key','jobnumber','occupationname','occupationtasksduties','isco','mjj3a',
                             'mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean']]
# ISIC main
isco_q1_main['mjj3cclean'] = isco_q1_main['mjj3cclean'].fillna(0).astype('int64').astype(str)
isco_q1_main['mjj3cclean'] = np.where(isco_q1_main.mjj3cclean.str.len() == 3, isco_q1_main.mjj3cclean.str.zfill(4), isco_q1_main.mjj3cclean)
isic_q1_main = pd.merge(isco_q1_main, isic, left_on='mjj3cclean', right_on='4-digits ', how='left')
isic_q1_main = isic_q1_main.rename(columns={'mjj3a':'activityname',
                                            'mjj3b':'activitygoodsservices'})
q1_main = isic_q1_main[['interview_key','jobnumber',
                        'occupationname','occupationtasksduties','isco',
                        'activityname','activitygoodsservices','isic']]
q1_main['jobnumber'] = 1
# ISCO second
isco_q1_second = pd.merge(q1_raw, isco, left_on='sjj1cclean', right_on='unit', how='left')
isco_q1_second = isco_q1_second[isco_q1_second.mjj1 == 2]
isco_q1_second = isco_q1_second.rename(columns={'mjj1':'jobnumber',
                                                'sjj1a':'occupationname',
                                                'sjj1b':'occupationtasksduties'})
isco_q1_second = isco_q1_second[['interview_key','jobnumber','occupationname','occupationtasksduties','isco','mjj3a',
                             'mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean']]
# ISIC second
isco_q1_second['sjj2cclean'] = isco_q1_second['sjj2cclean'].fillna(0).astype('int64').astype(str)
isco_q1_second['sjj2cclean'] = np.where(isco_q1_second.sjj2cclean.str.len() == 3, isco_q1_second.sjj2cclean.str.zfill(4), isco_q1_second.sjj2cclean)
isic_q1_second = pd.merge(isco_q1_second, isic, left_on='sjj2cclean', right_on='4-digits ', how='left')
isic_q1_second = isic_q1_second.rename(columns={'sjj2a':'activityname',
                                                'sjj2b':'activitygoodsservices'})
q1_second = isic_q1_second[['interview_key','jobnumber',
                        'occupationname','occupationtasksduties','isco',
                        'activityname','activitygoodsservices','isic']]
q1 = pd.concat([q1_main, q1_second], ignore_index=True)
q1 = q1[q1[['isco','isic']].notnull().all(axis=1)]
q1.to_csv('../pre-processed/NLFS_2024Q1.csv', index=False)

# Nigeria Labour Force Survey Q2 2024
# https://microdata.nigerianstat.gov.ng/index.php/catalog/152
#%%
q2_raw, meta = pyreadstat.read_sav('NLFS_2024Q2_INDIVIDUAL.sav',
                                   encoding='utf-8',
                                   usecols=['interview_key','mjj1','mjj2a','mjj2b','mjj2cclean','sjj1a','sjj1b','sjj1cclean',
                                            'mjj3a','mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean'])
# ISCO main
isco_q2_main = pd.merge(q2_raw, isco, left_on='mjj2cclean', right_on='unit', how='left')
isco_q2_main = isco_q2_main[isco_q2_main['mjj1'].notnull()]
isco_q2_main = isco_q2_main.rename(columns={'mjj1':'jobnumber',
                                            'mjj2a':'occupationname',
                                            'mjj2b':'occupationtasksduties'})
isco_q2_main = isco_q2_main[['interview_key','jobnumber','occupationname','occupationtasksduties','isco','mjj3a',
                             'mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean']]
# ISIC main
isco_q2_main['mjj3cclean'] = isco_q2_main['mjj3cclean'].fillna(0).astype('int64').astype(str)
isco_q2_main['mjj3cclean'] = np.where(isco_q2_main.mjj3cclean.str.len() == 3, isco_q2_main.mjj3cclean.str.zfill(4), isco_q2_main.mjj3cclean)
isic_q2_main = pd.merge(isco_q2_main, isic, left_on='mjj3cclean', right_on='4-digits ', how='left')
isic_q2_main = isic_q2_main.rename(columns={'mjj3a':'activityname',
                                            'mjj3b':'activitygoodsservices'})
q2_main = isic_q2_main[['interview_key','jobnumber',
                        'occupationname','occupationtasksduties','isco',
                        'activityname','activitygoodsservices','isic']]
q2_main['jobnumber'] = 1
# ISCO second
isco_q2_second = pd.merge(q2_raw, isco, left_on='sjj1cclean', right_on='unit', how='left')
isco_q2_second = isco_q2_second[isco_q2_second.mjj1 == 2]
isco_q2_second = isco_q2_second.rename(columns={'mjj1':'jobnumber',
                                                'sjj1a':'occupationname',
                                                'sjj1b':'occupationtasksduties'})
isco_q2_second = isco_q2_second[['interview_key','jobnumber','occupationname','occupationtasksduties','isco','mjj3a',
                             'mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean']]
# ISIC second
isco_q2_second['sjj2cclean'] = isco_q2_second['sjj2cclean'].fillna(0).astype('int64').astype(str)
isco_q2_second['sjj2cclean'] = np.where(isco_q2_second.sjj2cclean.str.len() == 3, isco_q2_second.sjj2cclean.str.zfill(4), isco_q2_second.sjj2cclean)
isic_q2_second = pd.merge(isco_q2_second, isic, left_on='sjj2cclean', right_on='4-digits ', how='left')
isic_q2_second = isic_q2_second.rename(columns={'sjj2a':'activityname',
                                                'sjj2b':'activitygoodsservices'})
q2_second = isic_q2_second[['interview_key','jobnumber',
                        'occupationname','occupationtasksduties','isco',
                        'activityname','activitygoodsservices','isic']]
q2 = pd.concat([q2_main, q2_second], ignore_index=True)
q2 = q2[q2[['isco','isic']].notnull().all(axis=1)]
q2.to_csv('../pre-processed/NLFS_2024Q2.csv', index=False)

# %%
