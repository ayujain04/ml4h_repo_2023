
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, kendalltau

# Function to annotate bars
def annotate_bars(bars, ax):
    for bar in bars:
        height = bar.get_height()
        if not np.isnan(height):  # Check if height is not NaN
            vertical_offset = 3 if height >= 0 else -15
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, vertical_offset),
                        textcoords="offset points",
                        ha='center', va='bottom')

# Load CSV files (Replace these paths with the paths to your own files)
df0 = pd.read_csv('path/to/combined_top_30_for_0_weighted_adj_matrix_embeddings.csv')
df1 = pd.read_csv('path/to/combined_top_30_for_1_weighted_adj_matrix_embeddings.csv')
df2 = pd.read_csv('path/to/combined_top_30_for_2_weighted_adj_matrix_embeddings.csv')
df3 = pd.read_csv('path/to/combined_top_30_for_3_weighted_adj_matrix_embeddings.csv')

# ... (you can insert the rank correlation calculation and plotting code here)

# Plotting code
fig, axes = plt.subplots(2, 2, figsize=(12, 12))
axes = axes.flatten()

# Loop through each effective percentage and plot the Spearman and Kendall correlations
for i, (percentage, data) in enumerate([(5, {}), (10, {}), (20, {}), (30, {})]):  # Replace these placeholders with your own data
    ax = axes[i]
    
    # Bar plot with hatch for Spearman
    bars_spearman = ax.bar(np.arange(3) - 0.2, [0.5, 0.6, 0.7], 0.4, label='Spearman', color='#377eb8', hatch='//')  # Replace these placeholders with your own data
    bars_kendall = ax.bar(np.arange(3) + 0.2, [0.4, 0.5, 0.6], 0.4, label='Kendall', color='#ff7f00')  # Replace these placeholders with your own data
    
    # Add annotations on bars
    annotate_bars(bars_spearman, ax)
    annotate_bars(bars_kendall, ax)
    
    # Add title
    ax.set_title(f'Top {percentage}%')
    
    # Add y-axis label only for the first column
    if i % 2 == 0:
        ax.set_ylabel('Rank Correlation')
        
    # Set x-ticks and x-tick labels
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(['(0)', '(1)', '(2)'])
    
    # Add legend only to the top-right subplot
    if i == 1:
        ax.legend(loc='upper right')

plt.tight_layout()
plt.show()
