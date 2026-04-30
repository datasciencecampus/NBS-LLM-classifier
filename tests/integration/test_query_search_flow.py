from __future__ import annotations

from pathlib import Path

import pandas as pd

from nbs_llm_classifier.query import build_queries
from nbs_llm_classifier.search import run_searches
from tests.helpers import (
    make_app_config,
    write_minimal_codebooks,
    write_minimal_prevalidated,
)


class FakeVectorStore:
    def __init__(self, kind: str) -> None:
        self.kind = kind

    @classmethod
    def from_filespace(cls, path: str, vectoriser):
        kind = "isco" if Path(path).name == "isco" else "isic"
        return cls(kind=kind)

    def search(self, search_input, n_results: int):
        ids = (
            search_input.get("id")
            if isinstance(search_input, dict)
            else search_input["id"]
        )
        primary = "5211" if self.kind == "isco" else "4711"
        secondary = "5221" if self.kind == "isco" else "4781"
        rows = []
        for query_id in ids:
            rows.append({"query_id": query_id, "doc_label": primary, "score": 0.9})
            rows.append({"query_id": query_id, "doc_label": secondary, "score": 0.8})
        return pd.DataFrame(rows)


def test_build_queries_then_run_search_with_mock_vectorstore(tmp_path, monkeypatch):
    config = make_app_config(tmp_path)
    write_minimal_prevalidated(config.paths.nlfs_prevalidated_csv, include_id=True)
    write_minimal_codebooks(config.paths.isco_xlsx, config.paths.isic_xlsx)

    build_queries(config)

    monkeypatch.setattr(
        "nbs_llm_classifier.search.create_vectoriser", lambda cfg: object()
    )
    monkeypatch.setattr("nbs_llm_classifier.search.VectorStore", FakeVectorStore)

    summary = run_searches(config)

    assert config.paths.search_results_isco_file.exists()
    assert config.paths.search_results_isic_file.exists()
    combined_file = config.paths.search_results_isco_file.with_name(
        "search_results_combined.csv"
    )
    assert combined_file.exists()

    isco_results = pd.read_csv(config.paths.search_results_isco_file, dtype=str)
    assert set(["id", "pred1", "pred1label", "match_top_1"]).issubset(
        isco_results.columns
    )
    assert summary["combined_file"] == "search_results_combined.csv"
