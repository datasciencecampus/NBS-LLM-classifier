from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.search import _combine_ranked_results, _format_code_label


def test_combine_ranked_results_builds_top3_correctly():
    search_results = pd.DataFrame(
        [
            {"query_id": "q1", "doc_label": "A", "score": 0.8},
            {"query_id": "q1", "doc_label": "A", "score": 0.9},
            {"query_id": "q1", "doc_label": "A", "score": 0.7},
            {"query_id": "q1", "doc_label": "B", "score": 0.5},
            {"query_id": "q1", "doc_label": "B", "score": 0.4},
            {"query_id": "q1", "doc_label": "C", "score": 0.3},
            {"query_id": "q2", "doc_label": "X", "score": 0.6},
        ]
    )

    combined = _combine_ranked_results(search_results)
    q1 = combined.loc[combined["query_id"] == "q1"].iloc[0]

    assert q1["pred1"] == "A"
    assert q1["pred2"] == "B"
    assert q1["pred3"] == "C"
    assert q1["score"] == 0.9


def test_format_code_label_handles_missing_values():
    descriptions = {"5211": "Stall and Market Salespersons"}

    assert (
        _format_code_label("5211", descriptions) == "5211 Stall and Market Salespersons"
    )
    assert _format_code_label("9999", descriptions) == "9999"
    assert _format_code_label(None, descriptions) == ""
