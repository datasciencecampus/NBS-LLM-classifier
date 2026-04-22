from __future__ import annotations

import pandas as pd

from nbs_llm_classifier.knowledgebase import build_knowledgebases
from tests.helpers import make_app_config, write_minimal_codebooks, write_minimal_q1


def test_build_knowledgebases_writes_expected_dictionary_files(tmp_path):
    config = make_app_config(tmp_path)
    write_minimal_codebooks(config.paths.isco_xlsx, config.paths.isic_xlsx)
    write_minimal_q1(config.paths.nlfs_q1_csv)

    summary = build_knowledgebases(config)

    assert config.paths.kb_isco_file.exists()
    assert config.paths.kb_isic_file.exists()

    kb_isco = pd.read_csv(config.paths.kb_isco_file, dtype=str)
    kb_isic = pd.read_csv(config.paths.kb_isic_file, dtype=str)

    assert list(kb_isco.columns) == ["label", "text"]
    assert list(kb_isic.columns) == ["label", "text"]
    assert not kb_isco.duplicated(subset=["label", "text"]).any()
    assert not kb_isic.duplicated(subset=["label", "text"]).any()
    assert summary["isco_rows"] == len(kb_isco)
    assert summary["isic_rows"] == len(kb_isic)
