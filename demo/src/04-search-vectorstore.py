# 04 - search vectorstore #

# Load libraries
import pandas as pd
import numpy as np

# Load vectoriser
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

# ISCO -----------------------------------------------------------------------
# Load vector store
from classifai.indexers import VectorStore
vector_store = VectorStore.from_filespace('../vector_store/isco', vectoriser)
# Load query
search_terms = pd.read_csv('../data/query_isco.csv', usecols=['id', 'query'])
# Search the vector store
from classifai.indexers.dataclasses import VectorStoreSearchInput
search_input = VectorStoreSearchInput(
    {"id": search_terms['id'].to_list(), 
    "query": search_terms['query'].to_list()}
)
search_results = vector_store.search(
  search_input, 
  n_results=15
  )
# Write results
search_results.to_csv('../data/isco_search_results.csv', index=False)

# ISIC -----------------------------------------------------------------------
# Load vector store
vector_store = VectorStore.from_filespace('../vector_store/isic', vectoriser)
# Load query
search_terms = pd.read_csv('../data/query_isic.csv', usecols=['id', 'query'])
# Search the vector store
search_input = VectorStoreSearchInput(
    {"id": search_terms['id'].to_list(), 
    "query": search_terms['query'].to_list()}
)
search_results = vector_store.search(
  search_input, 
  n_results=15
  )
# Write results
search_results.to_csv('../data/isic_search_results.csv', index=False)
