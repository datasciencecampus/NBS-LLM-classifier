from __future__ import annotations

import argparse
from pathlib import Path
from time import perf_counter
from typing import Callable

from nbs_llm_classifier.config import load_config
from nbs_llm_classifier.knowledgebase import build_knowledgebases
from nbs_llm_classifier.utils import ProgressReporter, StageContext
from nbs_llm_classifier.vectorstore import build_vectorstores
from nbs_llm_classifier.query import build_queries
from nbs_llm_classifier.search import run_searches
from nbs_llm_classifier.evaluate import evaluate_search_results


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NBS LLM classifier pipeline")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.json"),
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--progress",
        choices=["quiet", "normal", "verbose"],
        default=None,
        help="Progress verbosity override (default: config value)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("knowledgebase", help="Build knowledge base dictionaries")
    subparsers.add_parser("vectorstore", help="Build vector stores")
    subparsers.add_parser("query", help="Build query files")
    subparsers.add_parser("search", help="Search vector stores")
    subparsers.add_parser("evaluate", help="Evaluate search results")
    subparsers.add_parser("all", help="Run full pipeline")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config = load_config(args.config)
    progress_level = args.progress or config.progress_verbosity
    reporter = ProgressReporter(verbosity=progress_level)

    stage_map: dict[str, Callable[..., dict[str, object]]] = {
        "knowledgebase": build_knowledgebases,
        "vectorstore": build_vectorstores,
        "query": build_queries,
        "search": run_searches,
        "evaluate": evaluate_search_results,
    }

    if args.command == "all":
        pipeline = [
            ("knowledgebase", build_knowledgebases),
            ("vectorstore", build_vectorstores),
            ("query", build_queries),
            ("search", run_searches),
            ("evaluate", evaluate_search_results),
        ]
    else:
        pipeline = [(args.command, stage_map[args.command])]

    total_stages = len(pipeline)
    reporter.pipeline_start(command=args.command, total_stages=total_stages)
    pipeline_start = perf_counter()

    try:
        for index, (stage_name, stage_fn) in enumerate(pipeline, start=1):
            context = StageContext(name=stage_name, current=index, total=total_stages)
            reporter.stage_start(context)
            stage_start = perf_counter()
            try:
                metrics = stage_fn(config, reporter=reporter)
                reporter.stage_complete(
                    context,
                    duration_seconds=perf_counter() - stage_start,
                    metrics=metrics,
                )
            except Exception as error:
                reporter.stage_failed(
                    context,
                    duration_seconds=perf_counter() - stage_start,
                    error=error,
                )
                raise
        reporter.pipeline_complete(duration_seconds=perf_counter() - pipeline_start)
    except Exception as error:
        reporter.pipeline_failed(
            duration_seconds=perf_counter() - pipeline_start,
            error=error,
        )
        raise


if __name__ == "__main__":
    main()
