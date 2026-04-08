from __future__ import annotations

from pathlib import Path
import pandas as pd

from classifai.indexers import VectorStore
from classifai.indexers.dataclasses import VectorStoreSearchInput

from .config import AppConfig
from .utils import ProgressReporter
from .vectorstore import create_vectoriser


def _combine_ranked_results(search_results: pd.DataFrame) -> pd.DataFrame:
    scores = (
        search_results[["query_id", "doc_label", "score"]]
        .groupby(["query_id", "doc_label"])["score"]
        .max()
        .reset_index()
    )

    unique = (
        search_results[["query_id", "doc_label"]]
        .groupby(["query_id"])["doc_label"]
        .value_counts()
        .reset_index()
        .drop(columns=["count"])
    )
    unique = unique.merge(scores, on=["query_id", "doc_label"], how="left")
    unique["rank"] = unique.groupby("query_id").cumcount()

    combined = (
        unique[unique["rank"] == 0]
        .rename(columns={"doc_label": "pred1"})
        .loc[:, ["query_id", "pred1", "score"]]
    )

    for rank, name in [(1, "pred2"), (2, "pred3")]:
        ranked = unique[unique["rank"] == rank].rename(columns={"doc_label": name})
        combined = combined.merge(ranked[["query_id", name]], on="query_id", how="left")

    combined["pred1"] = combined["pred1"].astype(str)
    if "pred2" in combined.columns:
        combined["pred2"] = combined["pred2"].astype(str)
    if "pred3" in combined.columns:
        combined["pred3"] = combined["pred3"].astype(str)

    return combined


def _run_search(
    config: AppConfig,
    vector_store: VectorStore,
    query_file: Path,
    output_file: Path,
    label: str,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    if reporter:
        reporter.step(
            stage="search",
            message=f"loading {label} query file",
            level="verbose",
        )
    search_terms = pd.read_csv(query_file, dtype=str)
    if not {"id", "query", "prevalidated"}.issubset(search_terms.columns):
        raise ValueError(
            "Query file must contain id, query, and prevalidated columns."
        )
    search_input = VectorStoreSearchInput(
        {"id": search_terms["id"].to_list(), "query": search_terms["query"].to_list()}
    )
    if reporter:
        reporter.step(
            stage="search",
            message=f"running {label} vector search",
            metrics={"queries": len(search_terms)},
        )
    search_results = vector_store.search(search_input, n_results=config.n_results)

    combined_results = _combine_ranked_results(search_results)
    if query_file == config.paths.query_isco_file:
        descriptions = _load_description_lookup(
            config.paths.isco_xlsx,
            sheet_name="ISCO_08",
            code_column="unit",
            description_column="description",
        )
    else:
        descriptions = _load_description_lookup(
            config.paths.isic_xlsx,
            sheet_name="ISIC_Rev_4",
            code_column="4-digits ",
            description_column="description",
        )
    for column in ["pred1", "pred2", "pred3"]:
        label_column = f"{column}label"
        combined_results[label_column] = combined_results[column].map(
            lambda code: _format_code_label(code, descriptions)
        )
    matched_results = search_terms.merge(
        combined_results, left_on="id", right_on="query_id", how="left"
    )
    matched_results["match_top_1"] = (
        matched_results["prevalidated"] == matched_results["pred1"]
    )
    matched_results.to_csv(output_file, index=False)

    top1 = matched_results["match_top_1"].fillna(False).astype(bool)
    top1_accuracy = float(top1.mean() * 100) if len(top1) else 0.0
    metrics = {
        "queries": len(search_terms),
        "top1_accuracy_pct": round(top1_accuracy, 2),
        "output": output_file.name,
    }
    if reporter:
        reporter.step(
            stage="search",
            message=f"{label} search output written",
            level="verbose",
            metrics=metrics,
        )
    return metrics


def run_searches(
    config: AppConfig,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    if reporter:
        reporter.step(
            stage="search",
            current=1,
            total=5,
            message="creating embedding vectoriser",
            level="verbose",
            metrics={"model": config.model_name},
        )
    vectoriser = create_vectoriser(config)

    if reporter:
        reporter.step(
            stage="search",
            current=2,
            total=5,
            message="loading ISCO vector store",
        )
    isco_store = VectorStore.from_filespace(
        str(config.paths.vector_store_dir / "isco"), vectoriser
    )
    isco_metrics = _run_search(
        config,
        isco_store,
        config.paths.query_isco_file,
        config.paths.search_results_isco_file,
        label="isco",
        reporter=reporter,
    )

    if reporter:
        reporter.step(
            stage="search",
            current=3,
            total=5,
            message="loading ISIC vector store",
        )
    isic_store = VectorStore.from_filespace(
        str(config.paths.vector_store_dir / "isic"), vectoriser
    )
    isic_metrics = _run_search(
        config,
        isic_store,
        config.paths.query_isic_file,
        config.paths.search_results_isic_file,
        label="isic",
        reporter=reporter,
    )

    if reporter:
        reporter.step(
            stage="search",
            current=4,
            total=5,
            message="combining ISCO and ISIC search outputs",
        )
    combined_output = config.paths.search_results_isco_file.with_name(
        "search_results_combined.csv"
    )
    _combine_search_outputs(
        config.paths.search_results_isco_file,
        config.paths.search_results_isic_file,
        combined_output,
    )

    summary = {
        "isco_top1_pct": isco_metrics["top1_accuracy_pct"],
        "isic_top1_pct": isic_metrics["top1_accuracy_pct"],
        "combined_file": combined_output.name,
    }
    if reporter:
        reporter.step(
            stage="search",
            current=5,
            total=5,
            message="search stage complete",
            level="verbose",
            metrics=summary,
        )
    return summary


def _combine_search_outputs(
    isco_file: Path,
    isic_file: Path,
    output_file: Path,
) -> None:
    isco_results = pd.read_csv(isco_file, dtype=str)
    isic_results = pd.read_csv(isic_file, dtype=str)

    join_keys = ["id"]
    if "jobnumber" in isco_results.columns and "jobnumber" in isic_results.columns:
        join_keys.append("jobnumber")

    combined = isco_results.merge(
        isic_results,
        on=join_keys,
        suffixes=("_isco", "_isic"),
        how="outer",
    )
    combined.to_csv(output_file, index=False)


def _load_description_lookup(
    file_path: Path,
    sheet_name: str,
    code_column: str,
    description_column: str,
) -> dict[str, str]:
    frame = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        dtype=str,
        usecols=[code_column, description_column],
    )
    frame = frame.dropna(subset=[code_column, description_column])
    frame[code_column] = frame[code_column].astype(str)
    frame[description_column] = frame[description_column].astype(str)
    return dict(zip(frame[code_column], frame[description_column]))


def _format_code_label(code: str, descriptions: dict[str, str]) -> str:
    if code is None:
        return ""
    description = descriptions.get(str(code))
    if not description:
        return str(code)
    return f"{code} {description}"
