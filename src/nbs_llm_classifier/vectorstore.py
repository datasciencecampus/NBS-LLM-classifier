from __future__ import annotations

import numpy as np
import pandas as pd
import truststore
from classifai.indexers import VectorStore
from classifai.vectorisers import HuggingFaceVectoriser

from .config import AppConfig
from .utils import ProgressReporter


class NormalizedHfVectoriser(HuggingFaceVectoriser):
    def transform(self, texts: str | list[str]) -> np.ndarray:
        raw_embeddings = super().transform(texts)
        return raw_embeddings / np.linalg.norm(raw_embeddings, axis=1, keepdims=True)


def create_vectoriser(config: AppConfig) -> NormalizedHfVectoriser:
    truststore.inject_into_ssl()
    return NormalizedHfVectoriser(
        model_name=config.model_name,
        tokenizer_kwargs={"trust_remote_code": True},
        model_kwargs={"trust_remote_code": True},
    )


def build_vectorstores(
    config: AppConfig,
    reporter: ProgressReporter | None = None,
) -> dict[str, object]:
    if reporter:
        reporter.step(
            stage="vectorstore",
            current=1,
            total=4,
            message="ensuring vector store directory",
            level="verbose",
        )
    config.paths.vector_store_dir.mkdir(parents=True, exist_ok=True)

    if reporter:
        reporter.step(
            stage="vectorstore",
            current=2,
            total=4,
            message="creating embedding vectoriser",
            level="verbose",
            metrics={"model": config.model_name},
        )
    vectoriser = create_vectoriser(config)

    kb_isco_rows = len(pd.read_csv(config.paths.kb_isco_file, dtype=str))
    if reporter:
        reporter.step(
            stage="vectorstore",
            current=3,
            total=4,
            message="building ISCO vector store",
            metrics={"rows": kb_isco_rows},
        )
    VectorStore(
        file_name=str(config.paths.kb_isco_file),
        data_type="csv",
        vectoriser=vectoriser,
        output_dir=str(config.paths.vector_store_dir / "isco"),
        overwrite=True,
    )

    kb_isic_rows = len(pd.read_csv(config.paths.kb_isic_file, dtype=str))
    if reporter:
        reporter.step(
            stage="vectorstore",
            current=4,
            total=4,
            message="building ISIC vector store",
            metrics={"rows": kb_isic_rows},
        )
    VectorStore(
        file_name=str(config.paths.kb_isic_file),
        data_type="csv",
        vectoriser=vectoriser,
        output_dir=str(config.paths.vector_store_dir / "isic"),
        overwrite=True,
    )

    return {
        "isco_dir": "vector_store/isco",
        "isic_dir": "vector_store/isic",
        "model": config.model_name,
    }
