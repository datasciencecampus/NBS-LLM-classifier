from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.knowledgebase import build_knowledgebases
from tests.helpers import make_app_config


def test_build_knowledgebases_writes_outputs_and_summary(tmp_path, monkeypatch):
    config = make_app_config(tmp_path)

    expected_isco = pd.DataFrame(
        [
            {"label": "5211", "text": "trader sales"},
        ]
    )
    expected_isic = pd.DataFrame(
        [
            {"label": "4711", "text": "retail store"},
            {"label": "0144", "text": "goat raising"},
        ]
    )

    monkeypatch.setattr(
        "nbs_llm_classifier.knowledgebase._build_isco_frame",
        lambda isco_xlsx, validated_csv: expected_isco,
    )
    monkeypatch.setattr(
        "nbs_llm_classifier.knowledgebase._build_isic_frame",
        lambda isic_xlsx, validated_csv: expected_isic,
    )

    summary = build_knowledgebases(config)

    assert config.paths.kb_isco_file.exists()
    assert config.paths.kb_isic_file.exists()

    written_isco = pd.read_csv(config.paths.kb_isco_file, dtype=str)
    written_isic = pd.read_csv(config.paths.kb_isic_file, dtype=str)

    assert written_isco.to_dict("records") == expected_isco.to_dict("records")
    assert written_isic.to_dict("records") == expected_isic.to_dict("records")

    assert summary == {
        "isco_rows": 1,
        "isic_rows": 2,
        "kb_isco_file": "kb_isco.csv",
        "kb_isic_file": "kb_isic.csv",
    }
