# 05 - evaluate #

# Load libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

# ISCO ---------------------------------------------------------

# Find top 3 search results and join with validated codes
search_results = pd.read_csv('../data/isco_search_results.csv')
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
validated = pd.read_csv('../data/query_isco.csv')
test_results = validated.merge(combined_results, left_on='id', right_on='query_id')
test_results.head()

# Overall accuracy
accuracy = (test_results['prediction_1'] == test_results['validated']).mean()*100
print(f'In {round(accuracy,1)}% of cases the predicted code matched the validated code.')

# Plot Coverage vs Accuracy
thresholds = np.arange(0, 1.05, 0.01)
results = []

for threshold in thresholds:
    covered = test_results.loc[test_results['score'] > threshold]
    coverage = len(covered) / len(test_results)
    accuracy = (covered['validated'] == covered['prediction_1']).mean()
    results.append({'threshold': threshold, 'coverage': coverage, 'accuracy': accuracy})

results_df = pd.DataFrame(results)

x = results_df['coverage']
y = results_df['accuracy']
z = results_df['threshold']
xs = np.sort(x)
ys = np.array(y)[np.argsort(x)]
zs = np.array(z)[np.argsort(x)]
x0 = 0.5
x1 = 0.8
y0 = np.interp(x0, xs, ys)
y1 = np.interp(x1, xs, ys)
z0 = np.interp(x0, xs, zs)
z1 = np.interp(x1, xs, zs)

sns.set_style('whitegrid', {'axes.grid' : False})
plt.figure(figsize=(10, 6))
sns.lineplot(x='coverage', y='accuracy', data=results_df, color='#212121')
plt.axvline(x=0.5, color='#cab2d6', ls=':', lw = 2, alpha = 0.8)
plt.axvline(x=0.8, color='#6a3d9a', ls=':', lw = 2, alpha = 0.8)
plt.axhline(y=y0, color='#cab2d6', ls=':', lw = 2, alpha = 0.8)
plt.axhline(y=y1, color='#6a3d9a', ls=':', lw = 2, alpha = 0.8)
plt.plot(x0, y0, marker='o', color='#cab2d6')
plt.plot(x1, y1, marker='o', color='#6a3d9a')
plt.title('Coverage vs. Accuracy for Different Similarity Thresholds', fontsize=14, weight='bold', y=1.055, loc='left')
plt.gcf().text(0.125, 0.9, 'Q2 2024 NLFS - (sentence-transformers/all-MiniLM-L6-v2)', fontsize=9, color='#666')
plt.xlabel('Coverage')
plt.ylabel('Accuracy')
plt.text(0.02, 0.04, 
         f'cov≈0.50> (thr={z0:.2f})\ncov≈0.80> (thr={z1:.2f})', 
         transform=plt.gca().transAxes,
         fontsize=10, color='black',
         bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.6'))
plt.gca().yaxis.set_major_formatter(FormatStrFormatter('% 1.2f'))
plt.gca().yaxis.set_ticks_position('none')
plt.gca().yaxis.tick_right()
plt.gca().yaxis.set_label_position('right')
plt.show()