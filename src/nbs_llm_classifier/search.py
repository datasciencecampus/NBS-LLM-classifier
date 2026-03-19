from __future__ import annotations

from pathlib import Path
import pandas as pd

from classifai.indexers import VectorStore
from classifai.indexers.dataclasses import VectorStoreSearchInput

from .config import AppConfig
from .vectorstore import create_vectoriser


def _combine_ranked_results(search_results: pd.DataFrame) -> pd.DataFrame:
    scores = (
        search_results[["query_id", "doc_id", "score"]]
        .groupby(["query_id", "doc_id"])["score"]
        .max()
        .reset_index()
    )

    unique = (
        search_results[["query_id", "doc_id"]]
        .groupby(["query_id"])["doc_id"]
        .value_counts()
        .reset_index()
        .drop(columns=["count"])
    )
    unique = unique.merge(scores, on=["query_id", "doc_id"], how="left")
    unique["rank"] = unique.groupby("query_id").cumcount()

    combined = (
        unique[unique["rank"] == 0]
        .rename(columns={"doc_id": "prediction_1"})
        .loc[:, ["query_id", "prediction_1", "score"]]
    )

    for rank, name in [(1, "prediction_2"), (2, "prediction_3")]:
        ranked = unique[unique["rank"] == rank].rename(columns={"doc_id": name})
        combined = combined.merge(ranked[["query_id", name]], on="query_id", how="left")

    combined["prediction_1"] = combined["prediction_1"].astype(str)
    if "prediction_2" in combined.columns:
        combined["prediction_2"] = combined["prediction_2"].astype(str)
    if "prediction_3" in combined.columns:
        combined["prediction_3"] = combined["prediction_3"].astype(str)

    return combined


def _run_search(
    config: AppConfig,
    vector_store: VectorStore,
    query_file: Path,
    output_file: Path,
) -> None:
    search_terms = pd.read_csv(query_file, usecols=["id", "query"], dtype=str)
    search_input = VectorStoreSearchInput(
        {"id": search_terms["id"].to_list(), "query": search_terms["query"].to_list()}
    )
    search_results = vector_store.search(search_input, n_results=config.n_results)

    combined_results = _combine_ranked_results(search_results)
    validated = pd.read_csv(query_file, dtype=str)
    matched_results = validated.merge(
        combined_results, left_on="id", right_on="query_id", how="left"
    )
    matched_results["match_top_1"] = (
        matched_results["validated"] == matched_results["prediction_1"]
    )
    matched_results.to_csv(output_file, index=False)


def run_searches(config: AppConfig) -> None:
    vectoriser = create_vectoriser(config)

    isco_store = VectorStore.from_filespace(
        str(config.paths.vector_store_dir / "isco"), vectoriser
    )
    _run_search(
        config,
        isco_store,
        config.paths.query_isco_file,
        config.paths.search_results_isco_file,
    )

    isic_store = VectorStore.from_filespace(
        str(config.paths.vector_store_dir / "isic"), vectoriser
    )
    _run_search(
        config,
        isic_store,
        config.paths.query_isic_file,
        config.paths.search_results_isic_file,
    )
