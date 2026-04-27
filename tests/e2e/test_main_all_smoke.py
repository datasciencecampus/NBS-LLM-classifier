from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

import main as pipeline_main
from tests.helpers import (
    make_app_config,
    write_minimal_codebooks,
    write_minimal_prevalidated,
    write_minimal_validated,
)


class FakeVectorStore:
    def __init__(self, *args, **kwargs) -> None:
        output_dir = kwargs.get("output_dir")
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            (output_path / "metadata.json").write_text("{}", encoding="utf-8")
            self.kind = output_path.name
        else:
            self.kind = kwargs.get("kind", "isco")

    @classmethod
    def from_filespace(cls, path: str, vectoriser):
        return cls(kind=Path(path).name)

    def search(self, search_input, n_results: int):
        if isinstance(search_input, dict):
            ids = search_input["id"]
        else:
            ids = search_input.get("id")

        primary = "5211" if self.kind == "isco" else "4711"
        secondary = "6121" if self.kind == "isco" else "0144"

        rows = []
        for query_id in ids:
            rows.append({"query_id": query_id, "doc_label": primary, "score": 0.95})
            rows.append({"query_id": query_id, "doc_label": primary, "score": 0.90})
            rows.append({"query_id": query_id, "doc_label": secondary, "score": 0.85})
        return pd.DataFrame(rows)


def _write_config_json(root: Path) -> Path:
    config = {
        "model_name": "test-model",
        "n_results": 3,
        "progress_verbosity": "quiet",
        "paths": {
            "data_dir": "data",
            "raw_dir": "data/input",
            "preprocessed_dir": "data/input",
            "dictionaries_dir": "data/knowledgebase",
            "vector_store_dir": "vector_store",
            "isco_xlsx": "data/input/ISCO.xlsx",
            "isic_xlsx": "data/input/ISIC.xlsx",
            "nlfs_validated_csv": "data/input/NLFS_2024Q1.csv",
            "nlfs_prevalidated_csv": "data/input/NLFS_2024Q2.csv",
            "query_isco_file": "data/query/query_isco.csv",
            "query_isic_file": "data/query/query_isic.csv",
            "search_results_isco_file": "outputs/search_results_isco.csv",
            "search_results_isic_file": "outputs/search_results_isic.csv",
            "kb_isco_file": "data/knowledgebase/kb_isco.csv",
            "kb_isic_file": "data/knowledgebase/kb_isic.csv",
        },
    }
    config_path = root / "config.json"
    config_path.write_text(json.dumps(config), encoding="utf-8")
    return config_path


def test_main_all_pipeline_smoke(tmp_path, monkeypatch):
    app_config = make_app_config(tmp_path, include_outputs_dir=True)
    write_minimal_codebooks(app_config.paths.isco_xlsx, app_config.paths.isic_xlsx)
    write_minimal_validated(app_config.paths.nlfs_validated_csv)
    write_minimal_prevalidated(app_config.paths.nlfs_prevalidated_csv, include_id=True)

    config_path = _write_config_json(tmp_path)

    monkeypatch.setattr("nbs_llm_classifier.vectorstore.create_vectoriser", lambda cfg: object())
    monkeypatch.setattr("nbs_llm_classifier.search.create_vectoriser", lambda cfg: object())
    monkeypatch.setattr("nbs_llm_classifier.vectorstore.VectorStore", FakeVectorStore)
    monkeypatch.setattr("nbs_llm_classifier.search.VectorStore", FakeVectorStore)
    monkeypatch.setattr(
        "nbs_llm_classifier.evaluate._evaluate_and_plot",
        lambda search_results, subtitle: float(
            round((search_results["pred1"] == search_results["prevalidated"]).mean() * 100, 2)
        ),
    )

    monkeypatch.setattr(
        pipeline_main,
        "_parse_args",
        lambda: argparse.Namespace(command="all", config=config_path, progress="quiet"),
    )

    pipeline_main.main()

    assert app_config.paths.kb_isco_file.exists()
    assert app_config.paths.kb_isic_file.exists()
    assert app_config.paths.query_isco_file.exists()
    assert app_config.paths.query_isic_file.exists()
    assert app_config.paths.search_results_isco_file.exists()
    assert app_config.paths.search_results_isic_file.exists()

    combined = app_config.paths.search_results_isco_file.with_name("search_results_combined.csv")
    assert combined.exists()
