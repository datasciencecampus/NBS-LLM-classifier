from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.evaluate import _coerce_results, evaluate_search_results
from tests.helpers import make_app_config


def test_coerce_results_normalises_evaluation_columns():
    results = pd.DataFrame(
        [
            {"pred1": "5211", "prevalidated": "5211", "score": "0.9"},
            {"pred1": None, "prevalidated": "0144", "score": "not-a-score"},
        ]
    )

    coerced = _coerce_results(results)

    assert coerced["pred1"].tolist() == ["5211", ""]
    assert coerced["prevalidated"].tolist() == ["5211", "0144"]
    assert coerced.loc[0, "score"] == 0.9
    assert pd.isna(coerced.loc[1, "score"])


def test_evaluate_search_results_reads_files_and_returns_top1_metrics(
    tmp_path,
    monkeypatch,
):
    config = make_app_config(tmp_path)
    config.paths.search_results_isco_file.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        [
            {"pred1": "5211", "prevalidated": "5211", "score": "0.9"},
            {"pred1": "6121", "prevalidated": "9999", "score": "0.2"},
        ]
    ).to_csv(config.paths.search_results_isco_file, index=False)
    pd.DataFrame(
        [
            {"pred1": "4711", "prevalidated": "4711", "score": "0.8"},
            {"pred1": "0144", "prevalidated": "0144", "score": "0.7"},
        ]
    ).to_csv(config.paths.search_results_isic_file, index=False)

    subtitles: list[str] = []

    def fake_evaluate_and_plot(search_results: pd.DataFrame, subtitle: str) -> float:
        subtitles.append(subtitle)
        assert pd.api.types.is_numeric_dtype(search_results["score"])
        if subtitle.startswith("ISIC"):
            assert search_results["pred1"].tolist() == ["4711", "0144"]
        return float(
            round(
                (search_results["pred1"] == search_results["prevalidated"]).mean()
                * 100,
                2,
            )
        )

    monkeypatch.setattr(
        "nbs_llm_classifier.evaluate._evaluate_and_plot",
        fake_evaluate_and_plot,
    )

    summary = evaluate_search_results(config)

    assert summary == {"isco_top1_pct": 50.0, "isic_top1_pct": 100.0}
    assert subtitles == [
        "ISCO Q2 2024 NLFS - (test-model)",
        "ISIC Q2 2024 NLFS - (test-model)",
    ]
