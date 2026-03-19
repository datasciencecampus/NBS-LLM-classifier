from __future__ import annotations

from pathlib import Path
import pandas as pd

from .config import AppConfig


def _build_isco_frame(isco_xlsx: Path, q1_csv: Path) -> pd.DataFrame:
    isco = pd.read_excel(isco_xlsx, sheet_name="ISCO_08", dtype=str)
    isco["id"] = isco["unit"]
    text_cols = ["major_label", "sub_major_label", "minor_label", "description"]
    isco[text_cols] = isco[text_cols].fillna("")
    isco["text"] = isco[text_cols].agg(" ".join, axis=1).str.strip().str.lower()
    isco = isco[["id", "text"]]

    q1_isco = pd.read_csv(
        q1_csv,
        usecols=[
            "interview_key",
            "jobnumber",
            "occupationname",
            "occupationtasksduties",
            "isco",
        ],
        dtype=str,
    )
    q1_isco["id"] = q1_isco["isco"].str.extract(r"(\d+)")
    q1_isco["text"] = (
        q1_isco["occupationname"].fillna("")
        + " "
        + q1_isco["occupationtasksduties"].fillna("")
    ).str.strip().str.lower()

    kb_isco = pd.concat([isco, q1_isco[["id", "text"]]], ignore_index=True)
    kb_isco = kb_isco.drop_duplicates(subset=["id", "text"], keep="first")
    return kb_isco


def _build_isic_frame(isic_xlsx: Path, q1_csv: Path) -> pd.DataFrame:
    isic = pd.read_excel(isic_xlsx, sheet_name="ISIC_Rev_4", dtype=str)
    isic["id"] = isic["4-digits "]
    text_cols = ["section_label", "division_label", "group_label", "description"]
    isic[text_cols] = isic[text_cols].fillna("")
    isic["text"] = isic[text_cols].agg(" ".join, axis=1).str.strip().str.lower()
    isic = isic[["id", "text"]]

    q1_isic = pd.read_csv(
        q1_csv,
        usecols=[
            "interview_key",
            "jobnumber",
            "activityname",
            "activitygoodsservices",
            "isic",
        ],
        dtype=str,
    )
    q1_isic["id"] = q1_isic["isic"].str.extract(r"(\d+)")
    q1_isic["text"] = (
        q1_isic["activityname"].fillna("")
        + " "
        + q1_isic["activitygoodsservices"].fillna("")
    ).str.strip().str.lower()

    kb_isic = pd.concat([isic, q1_isic[["id", "text"]]], ignore_index=True)
    kb_isic = kb_isic.drop_duplicates(subset=["id", "text"], keep="first")
    return kb_isic


def build_knowledgebases(config: AppConfig) -> None:
    config.paths.dictionaries_dir.mkdir(parents=True, exist_ok=True)

    kb_isco = _build_isco_frame(config.paths.isco_xlsx, config.paths.nlfs_q1_csv)
    kb_isco.to_csv(config.paths.kb_isco_file, columns=["id", "text"], index=False)

    kb_isic = _build_isic_frame(config.paths.isic_xlsx, config.paths.nlfs_q1_csv)
    kb_isic.to_csv(config.paths.kb_isic_file, columns=["id", "text"], index=False)
