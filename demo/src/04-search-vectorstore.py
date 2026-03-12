# Search vectorstore

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

# ISCO ----------------------------------------------------------------------------
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

# Post-processing
search_results_scores = search_results[['query_id','doc_id','score']].groupby(['query_id','doc_id'])['score'].max().reset_index()
search_results_unique = pd.DataFrame(search_results[['query_id','doc_id']].groupby(['query_id'])['doc_id'].value_counts()).reset_index().drop('count', axis=1)
search_results_unique = search_results_unique.merge(search_results_scores, left_on=['query_id', 'doc_id'], right_on=['query_id', 'doc_id'])
search_results_unique['rank'] = search_results_unique.groupby('query_id')['doc_id'].cumcount()
search_results_0 = search_results_unique[search_results_unique['rank'] == 0].rename(columns={'doc_id': 'prediction_1'})
search_results_1 = search_results_unique[search_results_unique['rank'] == 1].rename(columns={'doc_id': 'prediction_2'})
search_results_2 = search_results_unique[search_results_unique['rank'] == 2].rename(columns={'doc_id': 'prediction_3'})
combined_results = search_results_0.merge(search_results_1[['query_id','prediction_2']], on='query_id', how='left')
combined_results = combined_results.merge(search_results_2[['query_id','prediction_3']], on='query_id', how='left')
combined_results = combined_results[['query_id','prediction_1','score','prediction_2','prediction_3']]
combined_results['prediction_2'] = combined_results['prediction_2'].astype('Int64')
combined_results['prediction_3'] = combined_results['prediction_3'].astype('Int64')
validated = pd.read_csv('../data/query_isco.csv', dtype = str)
matched_results = validated.merge(combined_results, left_on='id', right_on='query_id')
matched_results['Match top 1'] = matched_results['validated'] == matched_results['prediction_1']
# Write results
matched_results.to_csv('../data/search_results_isco.csv', index=False)

# ISIC ----------------------------------------------------------------------------
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

# Post-processing
search_results_scores = search_results[['query_id','doc_id','score']].groupby(['query_id','doc_id'])['score'].max().reset_index()
search_results_unique = pd.DataFrame(search_results[['query_id','doc_id']].groupby(['query_id'])['doc_id'].value_counts()).reset_index().drop('count', axis=1)
search_results_unique = search_results_unique.merge(search_results_scores, left_on=['query_id', 'doc_id'], right_on=['query_id', 'doc_id'])
search_results_unique['rank'] = search_results_unique.groupby('query_id')['doc_id'].cumcount()
search_results_0 = search_results_unique[search_results_unique['rank'] == 0].rename(columns={'doc_id': 'prediction_1'})
search_results_1 = search_results_unique[search_results_unique['rank'] == 1].rename(columns={'doc_id': 'prediction_2'})
search_results_2 = search_results_unique[search_results_unique['rank'] == 2].rename(columns={'doc_id': 'prediction_3'})
combined_results = search_results_0.merge(search_results_1[['query_id','prediction_2']], on='query_id', how='left')
combined_results = combined_results.merge(search_results_2[['query_id','prediction_3']], on='query_id', how='left')
combined_results = combined_results[['query_id','prediction_1','score','prediction_2','prediction_3']]
combined_results['prediction_2'] = combined_results['prediction_2'].astype('Int64')
combined_results['prediction_3'] = combined_results['prediction_3'].astype('Int64')
validated = pd.read_csv('../data/query_isic.csv', dtype = str)
matched_results = validated.merge(combined_results, left_on='id', right_on='query_id')
matched_results['Match top 1'] = matched_results['validated'] == matched_results['prediction_1']
# Write results
matched_results.to_csv('../data/search_results_isic.csv', index=False)
