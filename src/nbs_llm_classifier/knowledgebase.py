"""Build ISCO and ISIC knowledge base tables from classification schemes and NLFS validated data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import AppConfig
from .utils import ProgressReporter


def _build_isco_frame(isco_xlsx: Path, validated_csv: Path) -> pd.DataFrame:
    """Construct the ISCO knowledge base dataframe from classification schemes and NLFS validated data."""
    isco = pd.read_excel(isco_xlsx, sheet_name="ISCO_08", dtype=str)
    isco["label"] = isco["unit"]
    text_cols = ["major_label", "sub_major_label", "minor_label", "description"]
    isco[text_cols] = isco[text_cols].fillna("")
    isco["text"] = isco[text_cols].agg(" ".join, axis=1).str.strip().str.lower()
    isco = isco[["label", "text"]]

    validated_isco = pd.read_csv(
        validated_csv,
        usecols=[
            "interview_id",
            "jobnumber",
            "occupationname",
            "occupationtasksduties",
            "isco",
        ],
        dtype=str,
    )
    validated_isco["label"] = validated_isco["isco"].str.extract(r"(\d+)")
    validated_isco["text"] = (
        validated_isco["occupationname"].fillna("")
        + " "
        + validated_isco["occupationtasksduties"].fillna("")
    ).str.strip().str.lower()

    # Blend taxonomy descriptions with observed survey phrasing for recall.
    kb_isco = pd.concat([isco, validated_isco[["label", "text"]]], ignore_index=True)
    kb_isco = kb_isco.drop_duplicates(subset=["label", "text"], keep="first")
    return kb_isco


def _build_isic_frame(isic_xlsx: Path, validated_csv: Path) -> pd.DataFrame:
    """Construct the ISIC knowledge base dataframe from classification schemes and NLFS validated data."""
    isic = pd.read_excel(isic_xlsx, sheet_name="ISIC_Rev_4", dtype=str)
    isic["label"] = isic["4-digits "].astype(str).str.zfill(4)
    text_cols = ["section_label", "division_label", "group_label", "description"]
    isic[text_cols] = isic[text_cols].fillna("")
    isic["text"] = isic[text_cols].agg(" ".join, axis=1).str.strip().str.lower()
    isic = isic[["label", "text"]]

    validated_isic = pd.read_csv(
        validated_csv,
        usecols=[
            "interview_id",
            "jobnumber",
            "activityname",
            "activitygoodsservices",
            "isic",
        ],
        dtype=str,
    )
    validated_isic["label"] = validated_isic["isic"].str.extract(r"(\d+)")[0].str.zfill(4)
    validated_isic["text"] = (
        validated_isic["activityname"].fillna("")
        + " "
        + validated_isic["activitygoodsservices"].fillna("")
    ).str.strip().str.lower()

    kb_isic = pd.concat([isic, validated_isic[["label", "text"]]], ignore_index=True)
    kb_isic = kb_isic.drop_duplicates(subset=["label", "text"], keep="first")
    return kb_isic


def build_knowledgebases(
    config: AppConfig,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    """Build and persist ISCO and ISIC knowledge base CSV files."""
    if reporter:
        reporter.step(
            stage="knowledgebase",
            current=1,
            total=4,
            message="ensuring dictionary output directory",
            level="verbose",
        )
    config.paths.dictionaries_dir.mkdir(parents=True, exist_ok=True)

    if reporter:
        reporter.step(
            stage="knowledgebase",
            current=2,
            total=4,
            message="building ISCO dictionary",
        )
    kb_isco = _build_isco_frame(config.paths.isco_xlsx, config.paths.nlfs_validated_csv)
    kb_isco.to_csv(config.paths.kb_isco_file, columns=["label", "text"], index=False)

    if reporter:
        reporter.step(
            stage="knowledgebase",
            current=3,
            total=4,
            message="building ISIC dictionary",
        )
    kb_isic = _build_isic_frame(config.paths.isic_xlsx, config.paths.nlfs_validated_csv)
    kb_isic.to_csv(config.paths.kb_isic_file, columns=["label", "text"], index=False)

    summary = {
        "isco_rows": len(kb_isco),
        "isic_rows": len(kb_isic),
        "kb_isco_file": config.paths.kb_isco_file.name,
        "kb_isic_file": config.paths.kb_isic_file.name,
    }
    if reporter:
        reporter.step(
            stage="knowledgebase",
            current=4,
            total=4,
            message="knowledge base files written",
            level="verbose",
            metrics=summary,
        )
    return summary
