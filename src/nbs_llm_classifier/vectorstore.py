from __future__ import annotations

import numpy as np
import truststore

from classifai.indexers import VectorStore
from classifai.vectorisers import HuggingFaceVectoriser

from .config import AppConfig


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


def build_vectorstores(config: AppConfig) -> None:
    config.paths.vector_store_dir.mkdir(parents=True, exist_ok=True)
    vectoriser = create_vectoriser(config)

    VectorStore(
        file_name=str(config.paths.kb_isco_file),
        data_type="csv",
        vectoriser=vectoriser,
        output_dir=str(config.paths.vector_store_dir / "isco"),
        overwrite=True,
    )

    VectorStore(
        file_name=str(config.paths.kb_isic_file),
        data_type="csv",
        vectoriser=vectoriser,
        output_dir=str(config.paths.vector_store_dir / "isic"),
        overwrite=True,
    )
