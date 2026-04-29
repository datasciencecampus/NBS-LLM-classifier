from __future__ import annotations

import pandas as pd
import pytest

from nbs_llm_classifier.knowledgebase import _build_isic_frame
from nbs_llm_classifier.query import build_queries
from tests.helpers import make_app_config, write_minimal_validated


def test_build_queries_requires_occupation_task_column(tmp_path):
    config = make_app_config(tmp_path)
    pd.DataFrame(
        [
            {
                "id": "row-1",
                "jobnumber": "1",
                "occupationname": "Trader",
                "isco": "5211",
                "activityname": "Retail",
                "activitygoodsservices": "Selling goods",
                "isic": "4711",
            }
        ]
    ).to_csv(config.paths.nlfs_prevalidated_csv, index=False)

    with pytest.raises(KeyError, match="occupationtasksduties"):
        build_queries(config)


def test_build_isic_frame_requires_four_digit_code_column(tmp_path):
    isic_xlsx = tmp_path / "ISIC.xlsx"
    validated_csv = tmp_path / "validated.csv"
    pd.DataFrame(
        [
            {
                "section_label": "G",
                "division_label": "Retail",
                "group_label": "Store retail",
                "description": "Retail sale in non-specialized stores",
            }
        ]
    ).to_excel(isic_xlsx, sheet_name="ISIC_Rev_4", index=False)
    write_minimal_validated(validated_csv)

    with pytest.raises(KeyError, match="4-digits"):
        _build_isic_frame(isic_xlsx, validated_csv)
