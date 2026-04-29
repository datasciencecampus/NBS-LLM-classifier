"""Configuration models and loader for the NBS classifier pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    """Filesystem locations used by each pipeline stage."""

    data_dir: Path
    raw_dir: Path
    preprocessed_dir: Path
    dictionaries_dir: Path
    vector_store_dir: Path
    isco_xlsx: Path
    isic_xlsx: Path
    nlfs_validated_csv: Path
    nlfs_prevalidated_csv: Path
    query_isco_file: Path
    query_isic_file: Path
    search_results_isco_file: Path
    search_results_isic_file: Path
    kb_isco_file: Path
    kb_isic_file: Path


@dataclass(frozen=True)
class AppConfig:
    """Top-level runtime configuration for the pipeline."""

    root_dir: Path
    model_name: str
    n_results: int
    progress_verbosity: str
    paths: Paths


def _resolve_path(root_dir: Path, value: str) -> Path:
    """Resolve a configuration path value relative to the config file directory."""
    return (root_dir / value).resolve()


def load_config(config_path: Path) -> AppConfig:
    """Load application configuration from a JSON file.

    Missing values are populated from sensible defaults, and all configured paths
    are resolved relative to the directory containing the configuration file.
    """
    config_path = config_path.resolve()
    with config_path.open("r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)

    path_data = data.get("paths", {})
    root_dir = config_path.parent

    def resolve(key: str, default: str) -> Path:
        return _resolve_path(root_dir, path_data.get(key, default))

    paths = Paths(
        data_dir=resolve("data_dir", "data"),
        raw_dir=resolve("raw_dir", "data/input"),
        preprocessed_dir=resolve("preprocessed_dir", "data/input"),
        dictionaries_dir=resolve("dictionaries_dir", "data/knowledgebase"),
        vector_store_dir=resolve("vector_store_dir", "vector_store"),
        isco_xlsx=resolve("isco_xlsx", "data/input/ISCO.xlsx"),
        isic_xlsx=resolve("isic_xlsx", "data/input/ISIC.xlsx"),
        nlfs_validated_csv=resolve("nlfs_validated_csv", "data/input/NLFS_2024Q1.csv"),
        nlfs_prevalidated_csv=resolve(
            "nlfs_prevalidated_csv", "data/input/NLFS_2024Q2.csv"
        ),
        query_isco_file=resolve("query_isco_file", "data/query/query_isco.csv"),
        query_isic_file=resolve("query_isic_file", "data/query/query_isic.csv"),
        search_results_isco_file=resolve(
            "search_results_isco_file", "outputs/search_results_isco.csv"
        ),
        search_results_isic_file=resolve(
            "search_results_isic_file", "outputs/search_results_isic.csv"
        ),
        kb_isco_file=resolve("kb_isco_file", "data/knowledgebase/kb_isco.csv"),
        kb_isic_file=resolve("kb_isic_file", "data/knowledgebase/kb_isic.csv"),
    )

    model_name = data.get("model_name", "sentence-transformers/all-MiniLM-L6-v2")
    n_results = int(data.get("n_results", 15))
    progress_verbosity = str(data.get("progress_verbosity", "normal")).lower()

    return AppConfig(
        root_dir=root_dir,
        model_name=model_name,
        n_results=n_results,
        progress_verbosity=progress_verbosity,
        paths=paths,
    )
