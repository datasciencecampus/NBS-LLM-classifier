# 02 - build vectorstore # 

# Load libraries
import numpy as np
import truststore

truststore.inject_into_ssl()

# Choose a vectoriser
from classifai.vectorisers import HuggingFaceVectoriser

class MyNormalisedHF_Vectoriser(HuggingFaceVectoriser):
    def transform(self, texts: str | list[str]) -> np.ndarray:
        raw_embeddings = super().transform(texts)
        return raw_embeddings/np.linalg.norm(raw_embeddings, axis=1, keepdims=True)

vectoriser = MyNormalisedHF_Vectoriser(
  model_name='sentence-transformers/all-MiniLM-L6-v2', # or 'nomic-ai/nomic-embed-text-v1.5'
  tokenizer_kwargs={"trust_remote_code":True},
  model_kwargs={"trust_remote_code":True}
)

# Build a vector store

# ISCO -----------------------------------------------------------------------
from classifai.indexers import VectorStore

vector_store = VectorStore(
  file_name='../data/dictionaries/kb_isco.csv',
  data_type='csv',
  vectoriser=vectoriser,
  output_dir='../vector_store/isco',
  overwrite=True
  )

# ISIC -----------------------------------------------------------------------
vector_store = VectorStore(
  file_name='../data/dictionaries/kb_isic.csv',
  data_type='csv',
  vectoriser=vectoriser,
  output_dir='../vector_store/isic',
  overwrite=True
  )
