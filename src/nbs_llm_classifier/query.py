"""Build ISCO and ISIC query files from prevalidated NLFS survey responses."""

from __future__ import annotations

import pandas as pd

from .config import AppConfig
from .utils import ProgressReporter


def build_queries(
    config: AppConfig,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    """Create ISCO and ISIC query CSV files from prevalidated NLFS responses.

    File inputs from ``config.paths``:
    - Reads ``nlfs_prevalidated_csv``.

    Expected input columns in ``nlfs_prevalidated_csv``:
    - Required for ISCO query generation: ``occupationname``,
      ``occupationtasksduties``, and ``isco``.
    - Required for ISIC query generation: ``activityname``,
      ``activitygoodsservices``, and ``isic``.
    - ``id`` is optional; if missing, sequential ids are synthesized.
    - ``jobnumber`` is expected because it is written to both outputs.

    File outputs:
    - Ensures parent directories for ``query_isco_file`` and ``query_isic_file``
      exist.
    - Writes both CSVs with columns ``id``, ``jobnumber``, ``query``, and
      ``prevalidated``.
    """
    if reporter:
        reporter.step(
            stage="query",
            current=1,
            total=4,
            message="loading prevalidated data",
        )
    prevalidated_data = pd.read_csv(config.paths.nlfs_prevalidated_csv, dtype=str)
    if "id" not in prevalidated_data.columns:
        # Preserve upstream ids when present; only synthesize sequential ids as fallback.
        prevalidated_data = prevalidated_data.assign(id=range(len(prevalidated_data)))

    if reporter:
        reporter.step(
            stage="query",
            current=2,
            total=4,
            message="building ISCO query file",
        )
    config.paths.query_isco_file.parent.mkdir(parents=True, exist_ok=True)
    query_isco = prevalidated_data.copy()
    query_isco["query"] = (
        (
            query_isco["occupationname"].fillna("")
            + " "
            + query_isco["occupationtasksduties"].fillna("")
        )
        .str.strip()
        .str.lower()
    )
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
    query_isic = prevalidated_data.copy()
    query_isic["query"] = (
        (
            query_isic["activityname"].fillna("")
            + " "
            + query_isic["activitygoodsservices"].fillna("")
        )
        .str.strip()
        .str.lower()
    )
    query_isic["prevalidated"] = query_isic["isic"].str.extract(r"(\d+)")
    query_isic.to_csv(
        config.paths.query_isic_file,
        columns=["id", "jobnumber", "query", "prevalidated"],
        index=False,
    )

    summary = {
        "rows": len(prevalidated_data),
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
