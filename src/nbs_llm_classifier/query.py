from __future__ import annotations

import pandas as pd

from .config import AppConfig


def build_queries(config: AppConfig) -> None:
    q2 = pd.read_csv(config.paths.nlfs_q2_csv, dtype=str)
    q2 = q2.assign(id=range(len(q2)))

    query_isco = q2.copy()
    query_isco["query"] = (
        query_isco["occupationname"].fillna("")
        + " "
        + query_isco["occupationtasksduties"].fillna("")
    ).str.strip().str.lower()
    query_isco["validated"] = query_isco["isco"].str.extract(r"(\d+)")
    query_isco.to_csv(
        config.paths.query_isco_file,
        columns=["id", "query", "validated"],
        index=False,
    )

    query_isic = q2.copy()
    query_isic["query"] = (
        query_isic["activityname"].fillna("")
        + " "
        + query_isic["activitygoodsservices"].fillna("")
    ).str.strip().str.lower()
    query_isic["validated"] = query_isic["isic"].str.extract(r"(\d+)")
    query_isic.to_csv(
        config.paths.query_isic_file,
        columns=["id", "query", "validated"],
        index=False,
    )
