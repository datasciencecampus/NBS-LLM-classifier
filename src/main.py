from __future__ import annotations

import argparse
from pathlib import Path

from nbs_llm_classifier.config import load_config
from nbs_llm_classifier.knowledgebase import build_knowledgebases
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

    if args.command == "knowledgebase":
        build_knowledgebases(config)
    elif args.command == "vectorstore":
        build_vectorstores(config)
    elif args.command == "query":
        build_queries(config)
    elif args.command == "search":
        run_searches(config)
    elif args.command == "evaluate":
        evaluate_search_results(config)
    elif args.command == "all":
        build_knowledgebases(config)
        build_vectorstores(config)
        build_queries(config)
        run_searches(config)
        evaluate_search_results(config)


if __name__ == "__main__":
    main()
