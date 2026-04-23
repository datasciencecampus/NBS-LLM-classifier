from __future__ import annotations

import pandas as pd

from .config import AppConfig
from .utils import ProgressReporter


def build_queries(
    config: AppConfig,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    if reporter:
        reporter.step(
            stage="query",
            current=1,
            total=4,
            message="loading Q2 pre-processed data",
        )
    q2 = pd.read_csv(config.paths.nlfs_q2_csv, dtype=str)
    if "id" not in q2.columns:
        q2 = q2.assign(id=range(len(q2)))

    if reporter:
        reporter.step(
            stage="query",
            current=2,
            total=4,
            message="building ISCO query file",
        )
    config.paths.query_isco_file.parent.mkdir(parents=True, exist_ok=True)
    query_isco = q2.copy()
    query_isco["query"] = (
        query_isco["occupationname"].fillna("")
        + " "
        + query_isco["occupationtasksduties"].fillna("")
    ).str.strip().str.lower()
    query_isco["prevalidated"] = query_isco["isco"].str.extract(r"(\d+)")
    query_isco.to_csv(
        config.paths.query_isco_file,
        columns=["id", "jobnumber", "query", "prevalidated"],
        index=False,
    )

    if reporter:
        reporter.step(
            stage="query",
            current=3,
            total=4,
            message="building ISIC query file",
        )
    config.paths.query_isic_file.parent.mkdir(parents=True, exist_ok=True)
    query_isic = q2.copy()
    query_isic["query"] = (
        query_isic["activityname"].fillna("")
        + " "
        + query_isic["activitygoodsservices"].fillna("")
    ).str.strip().str.lower()
    query_isic["prevalidated"] = query_isic["isic"].str.extract(r"(\d+)")
    query_isic.to_csv(
        config.paths.query_isic_file,
        columns=["id", "jobnumber", "query", "prevalidated"],
        index=False,
    )

    summary = {
        "rows": len(q2),
        "query_isco_file": config.paths.query_isco_file.name,
        "query_isic_file": config.paths.query_isic_file.name,
    }
    if reporter:
        reporter.step(
            stage="query",
            current=4,
            total=4,
            message="query files written",
            level="verbose",
            metrics=summary,
        )
    return summary
