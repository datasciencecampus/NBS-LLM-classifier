# Datasets

The following datasets have been used in this demo:

|Name |Source |URL |Type |
|:-----|:-----|:-----|:-----|
| International Standard Classification of Occupations | International Labour Organization (ISCO) | [Link](https://www.ilo.org/ilostat-files/Documents/ISCO.xlsx) | .xlsx (81KB) |
| International Standard Industrial Classification of All Economic Activities (ISIC) | International Labour Organization (ISCO) | [Link](http://www.ilo.org/ilostat-files/Documents/ISIC.xlsx) | .xlsx (107KB) |
| Nigeria Labour Force Survey Q1 2024 | Nigeria National Bureau of Statistics | [Link](https://microdata.nigerianstat.gov.ng/index.php/catalog/151) | |
| Nigeria Labour Force Survey Q2 2024 | Nigeria National Bureau of Statistics | [Link](https://microdata.nigerianstat.gov.ng/index.php/catalog/152) | |

The quarterly data from the Nigeria Labour Force Survey are subsets of those published on the [Microdata Catalog](https://microdata.nigerianstat.gov.ng/index.php/home). Only the columns `['interview_key','mjj1','mjj2a','mjj2b','mjj2cclean','sjj1a','sjj1b','sjj1cclean', 'mjj3a','mjj3b','mjj3cclean','sjj2a','sjj2b','sjj2cclean']` which refer to ISCO and ISIC classified main and secondary jobs were retained. The data have been cleaned and converted to long format.