# 03 - build input query #

# Load libraries
import pandas as pd

# Q2 2024 NLFS
# Source: Nigeria National Bureau of Statistics
# URL: https://microdata.nigerianstat.gov.ng/index.php/catalog/152

# ISCO -----------------------------------------------------------------------
query_isco = pd.read_csv("../data/pre-processed/NLFS_2024Q2.csv")
query_isco = query_isco.assign(id=range(len(query_isco)))
query_isco["query"] = (
    query_isco["occupationname"] + " " + query_isco["occupationtasksduties"]
)
query_isco["query"] = query_isco["query"].str.lower()
query_isco["validated"] = query_isco["isco"].str.extract(r"(\d+)")
query_isco.to_csv(
    "../data/query_isco.csv", columns=["id", "query", "validated"], index=False
)

# ISIC -----------------------------------------------------------------------
query_isic = pd.read_csv("../data/pre-processed/NLFS_2024Q2.csv")
query_isic = query_isic.assign(id=range(len(query_isic)))
query_isic["query"] = (
    query_isic["activityname"] + " " + query_isic["activitygoodsservices"]
)
query_isic["query"] = query_isic["query"].str.lower()
query_isic["validated"] = query_isic["isic"].str.extract(r"(\d+)")
query_isic.to_csv(
    "../data/query_isic.csv", columns=["id", "query", "validated"], index=False
)
