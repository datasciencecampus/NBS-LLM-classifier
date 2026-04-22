from __future__ import annotations

from pathlib import Path
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _ensure_truststore_stub() -> None:
    try:
        import truststore  # noqa: F401
    except Exception:
        module = types.ModuleType("truststore")
        module.inject_into_ssl = lambda: None
        sys.modules["truststore"] = module


def _ensure_classifai_stub() -> None:
    try:
        import classifai  # noqa: F401
    except Exception:
        classifai_module = types.ModuleType("classifai")
        indexers_module = types.ModuleType("classifai.indexers")
        dataclasses_module = types.ModuleType("classifai.indexers.dataclasses")
        vectorisers_module = types.ModuleType("classifai.vectorisers")

        class StubVectorStore:
            def __init__(self, *args, **kwargs) -> None:
                pass

            @classmethod
            def from_filespace(cls, *args, **kwargs):
                return cls()

            def search(self, *args, **kwargs):
                raise NotImplementedError("Stub VectorStore.search called")

        class StubVectorStoreSearchInput(dict):
            def __init__(self, payload):
                super().__init__(payload)

        class StubHuggingFaceVectoriser:
            def __init__(self, *args, **kwargs) -> None:
                pass

            def transform(self, texts):
                raise NotImplementedError("Stub vectoriser has no transform")

        indexers_module.VectorStore = StubVectorStore
        dataclasses_module.VectorStoreSearchInput = StubVectorStoreSearchInput
        vectorisers_module.HuggingFaceVectoriser = StubHuggingFaceVectoriser

        classifai_module.indexers = indexers_module
        classifai_module.vectorisers = vectorisers_module

        sys.modules["classifai"] = classifai_module
        sys.modules["classifai.indexers"] = indexers_module
        sys.modules["classifai.indexers.dataclasses"] = dataclasses_module
        sys.modules["classifai.vectorisers"] = vectorisers_module


_ensure_truststore_stub()
_ensure_classifai_stub()
