# 01 - create knowledgebase #

# Load libraries
import pandas as pd
import numpy as np

# ISCO -----------------------------------------------------------------------

# ISCO code scheme
# Source: International Labour Organization (ISCO) 
# URL: https://www.ilo.org/ilostat-files/Documents/ISCO.xlsx
isco = pd.read_excel('../data/raw/ISCO.xlsx', sheet_name = 'ISCO_08', dtype = str)
isco['id'] = isco['unit']
isco['text'] = isco['major_label'] + ' ' + isco['sub_major_label'] + ' ' + isco['minor_label'] + ' ' + isco['description']
isco['text'] = isco['text'].str.lower()
isco = isco[['id', 'text']]
isco.head()

# Q1 2025 NLFS
# Source: Nigeria National Bureau of Statistics
# URL: https://microdata.nigerianstat.gov.ng/index.php/catalog/151
q1_isco = pd.read_csv('../data/pre-processed/NLFS_2024Q1.csv',
                      usecols=['interview_key','jobnumber','occupationname','occupationtasksduties','isco'])
q1_isco['id'] = q1_isco['isco'].str.extract('(\d+)')
q1_isco['text'] = q1_isco['occupationname'] + ' ' + q1_isco['occupationtasksduties']
q1_isco['text'] = q1_isco['text'].str.lower()
q1_isco.head()

# Combine ISCO scheme and labelled data
kb_isco = pd.concat([isco, q1_isco[['id','text']]])
kb_isco = kb_isco.drop_duplicates(subset=['id' and 'text'], keep='first', inplace=False)
kb_isco.to_csv('../data/dictionaries/kb_isco.csv', columns=['id','text'], index=False)

# ISIC -----------------------------------------------------------------------

# ISIC code scheme
# Source: International Labour Organization (ISCO) 
# URL: http://www.ilo.org/ilostat-files/Documents/ISIC.xlsx
isic = pd.read_excel('../data/raw/ISIC.xlsx', sheet_name = 'ISIC_Rev_4', dtype = str)
isic['id'] = isic['4-digits ']
isic['text'] = isic['section_label'] + ' ' + isic['division_label'] + ' ' + isic['group_label'] + ' ' + isic['description']
isic['text'] = isic['text'].str.lower()
isic = isic[['id', 'text']]
isic.head()

# Q1 2025 NLFS
# Source: Nigeria National Bureau of Statistics
# URL: https://microdata.nigerianstat.gov.ng/index.php/catalog/151
q1_isic = pd.read_csv('../data/pre-processed/NLFS_2024Q1.csv',
                      usecols=['interview_key','jobnumber','activityname','activitygoodsservices','isic'])
q1_isic['id'] = q1_isic['isic'].str.extract('(\d+)')
q1_isic['text'] = q1_isic['activityname'] + ' ' + q1_isic['activitygoodsservices']
q1_isic['text'] = q1_isic['text'].str.lower()
q1_isic.head()

# Combine ISIC scheme and labelled data
kb_isic = pd.concat([isic, q1_isic[['id','text']]])
kb_isic = kb_isic.drop_duplicates(subset=['id' and 'text'], keep='first', inplace=False)
kb_isic.to_csv('../data/dictionaries/kb_isic.csv', columns=['id','text'], index=False)
