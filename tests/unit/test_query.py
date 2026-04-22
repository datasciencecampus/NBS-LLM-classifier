from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.query import build_queries
from tests.helpers import make_app_config, write_minimal_q2


def test_query_preserves_existing_id(tmp_path):
    config = make_app_config(tmp_path)
    write_minimal_q2(config.paths.nlfs_q2_csv, include_id=True)

    build_queries(config)

    isco_query = pd.read_csv(config.paths.query_isco_file, dtype=str)
    isic_query = pd.read_csv(config.paths.query_isic_file, dtype=str)

    assert isco_query["id"].tolist() == ["row-1", "row-2"]
    assert isic_query["id"].tolist() == ["row-1", "row-2"]


def test_query_generates_fallback_id_when_missing(tmp_path):
    config = make_app_config(tmp_path)
    write_minimal_q2(config.paths.nlfs_q2_csv, include_id=False)

    build_queries(config)

    isco_query = pd.read_csv(config.paths.query_isco_file, dtype=str)
    assert isco_query["id"].tolist() == ["0", "1"]
    assert list(isco_query.columns) == ["id", "jobnumber", "query", "prevalidated"]
