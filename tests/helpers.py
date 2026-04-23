from __future__ import annotations

from pathlib import Path

import pandas as pd

from nbs_llm_classifier.config import AppConfig, Paths


def make_app_config(tmp_path: Path, include_outputs_dir: bool = True) -> AppConfig:
    data_dir = tmp_path / "data"
    raw_dir = data_dir / "input"
    preprocessed_dir = data_dir / "input"
    dictionaries_dir = data_dir / "knowledgebase"
    query_dir = data_dir / "query"
    vector_store_dir = tmp_path / "vector_store"
    outputs_dir = tmp_path / "outputs"

    raw_dir.mkdir(parents=True, exist_ok=True)
    preprocessed_dir.mkdir(parents=True, exist_ok=True)
    dictionaries_dir.mkdir(parents=True, exist_ok=True)
    query_dir.mkdir(parents=True, exist_ok=True)
    vector_store_dir.mkdir(parents=True, exist_ok=True)
    if include_outputs_dir:
        outputs_dir.mkdir(parents=True, exist_ok=True)

    paths = Paths(
        data_dir=data_dir,
        raw_dir=raw_dir,
        preprocessed_dir=preprocessed_dir,
        dictionaries_dir=dictionaries_dir,
        vector_store_dir=vector_store_dir,
        isco_xlsx=raw_dir / "ISCO.xlsx",
        isic_xlsx=raw_dir / "ISIC.xlsx",
        nlfs_q1_csv=preprocessed_dir / "NLFS_2024Q1.csv",
        nlfs_q2_csv=preprocessed_dir / "NLFS_2024Q2.csv",
        query_isco_file=query_dir / "query_isco.csv",
        query_isic_file=query_dir / "query_isic.csv",
        search_results_isco_file=outputs_dir / "search_results_isco.csv",
        search_results_isic_file=outputs_dir / "search_results_isic.csv",
        kb_isco_file=dictionaries_dir / "kb_isco.csv",
        kb_isic_file=dictionaries_dir / "kb_isic.csv",
    )

    return AppConfig(
        root_dir=tmp_path,
        model_name="test-model",
        n_results=3,
        progress_verbosity="quiet",
        paths=paths,
    )


def write_minimal_q1(path: Path) -> None:
    frame = pd.DataFrame(
        [
            {
                "interview_id": "int-1",
                "jobnumber": "1",
                "occupationname": "Trader",
                "occupationtasksduties": "Sells goods",
                "isco": "5211",
                "activityname": "Retail sale",
                "activitygoodsservices": "Sells goods",
                "isic": "4711",
            },
            {
                "interview_id": "int-2",
                "jobnumber": "2",
                "occupationname": "Livestock farmer",
                "occupationtasksduties": "Raises goats",
                "isco": "6121",
                "activityname": "Sheep and goat raising",
                "activitygoodsservices": "Raises goats",
                "isic": "0144",
            },
            {
                "interview_id": "int-2",
                "jobnumber": "2",
                "occupationname": "Livestock farmer",
                "occupationtasksduties": "Raises goats",
                "isco": "6121",
                "activityname": "Sheep and goat raising",
                "activitygoodsservices": "Raises goats",
                "isic": "0144",
            },
        ]
    )
    frame.to_csv(path, index=False)


def write_minimal_q2(path: Path, include_id: bool) -> None:
    rows = [
        {
            "id": "row-1",
            "jobnumber": "1",
            "occupationname": "Trader",
            "occupationtasksduties": "Selling market items",
            "isco": "5211",
            "activityname": "Retail",
            "activitygoodsservices": "Selling food and soap",
            "isic": "4711",
        },
        {
            "id": "row-2",
            "jobnumber": "2",
            "occupationname": "Goat farmer",
            "occupationtasksduties": "Raising goats",
            "isco": "6121",
            "activityname": "Goat raising",
            "activitygoodsservices": "Raising and selling goats",
            "isic": "0144",
        },
    ]
    frame = pd.DataFrame(rows)
    if not include_id:
        frame = frame.drop(columns=["id"])
    frame.to_csv(path, index=False)


def write_minimal_codebooks(isco_path: Path, isic_path: Path) -> None:
    isco = pd.DataFrame(
        [
            {
                "unit": "5211",
                "major_label": "Sales",
                "sub_major_label": "Market sales",
                "minor_label": "Stalls",
                "description": "Stall and market salespersons",
            },
            {
                "unit": "6121",
                "major_label": "Agriculture",
                "sub_major_label": "Livestock",
                "minor_label": "Goats",
                "description": "Livestock and dairy producers",
            },
        ]
    )

    isic = pd.DataFrame(
        [
            {
                "4-digits ": "4711",
                "section_label": "G",
                "division_label": "Retail",
                "group_label": "Store retail",
                "description": "Retail sale in non-specialized stores",
            },
            {
                "4-digits ": "0144",
                "section_label": "A",
                "division_label": "Agriculture",
                "group_label": "Animal production",
                "description": "Raising of sheep and goats",
            },
        ]
    )

    with pd.ExcelWriter(isco_path, engine="openpyxl") as writer:
        isco.to_excel(writer, sheet_name="ISCO_08", index=False)

    with pd.ExcelWriter(isic_path, engine="openpyxl") as writer:
        isic.to_excel(writer, sheet_name="ISIC_Rev_4", index=False)
