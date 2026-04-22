from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.search import _combine_search_outputs


def test_combine_search_outputs_applies_schema_and_order(tmp_path):
    isco_file = tmp_path / "search_results_isco.csv"
    isic_file = tmp_path / "search_results_isic.csv"
    output_file = tmp_path / "search_results_combined.csv"

    isco = pd.DataFrame(
        [
            {
                "id": "row-1",
                "jobnumber": "1",
                "query_id": "row-1",
                "query": "isco text",
                "prevalidated": "5211",
                "pred1": "5211",
                "score": "0.95",
                "pred1label": "5211 Stall and Market Salespersons",
                "pred2": "5221",
                "pred2label": "5221 Shopkeepers",
                "pred3": "5230",
                "pred3label": "5230 Cashiers",
                "match_top_1": "True",
            }
        ]
    )
    isic = pd.DataFrame(
        [
            {
                "id": "row-1",
                "jobnumber": "1",
                "query_id": "row-1",
                "query": "isic text",
                "prevalidated": "4711",
                "pred1": "4711",
                "score": "0.91",
                "pred1label": "4711 Retail sale in non-specialized stores",
                "pred2": "4781",
                "pred2label": "4781 Retail sale via stalls",
                "pred3": "4721",
                "pred3label": "4721 Retail sale of food",
                "match_top_1": "True",
            }
        ]
    )

    isco.to_csv(isco_file, index=False)
    isic.to_csv(isic_file, index=False)

    _combine_search_outputs(isco_file, isic_file, output_file)

    combined = pd.read_csv(output_file, dtype=str)

    expected_prefix = [
        "id",
        "job_number",
        "isco_query_id",
        "isco_query",
        "isco_prevalidated",
        "isco_pred1",
        "isco_pred1_label",
        "isco_pred1_score",
    ]
    assert combined.columns[: len(expected_prefix)].tolist() == expected_prefix
    assert combined.loc[0, "isco_pred1"] == "5211"
    assert combined.loc[0, "isic_pred1"] == "4711"
