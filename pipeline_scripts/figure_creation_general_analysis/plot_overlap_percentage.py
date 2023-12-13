
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to get the top x% nodes based on cosine similarity
def get_top_x_percent_nodes(df, x_percent):
    total_count = len(df)
    top_count = int(np.ceil(total_count * (x_percent / 100)))
    top_nodes = df.nlargest(top_count, 'Cosine Similarity')['Queried Node'].unique()
    return set(top_nodes)

# Function to calculate the percentage overlap between two sets
def calculate_overlap_percent(set1, set2):
    overlap = len(set1.intersection(set2))
    total = len(set1)
    if total == 0:
        return 0
    return (overlap / total) * 100

# Load the top 30% embeddings CSV files
file_paths_embeddings = {
    0: '../combined_top_30_for_0_weighted_adj_matrix_embeddings.csv',
    1: '../combined_top_30_for_1_weighted_adj_matrix_embeddings.csv',
    2: '../combined_top_30_for_2_weighted_adj_matrix_embeddings.csv',
    3: '../combined_top_30_for_3_weighted_adj_matrix_embeddings.csv'
}

# Dictionary to store the top 30% embeddings data for each graph
top_30_embeddings = {}

# Load each file and store the data
for i, file_path in file_paths_embeddings.items():
    top_30_embeddings[i] = pd.read_csv(file_path)

# Dictionary to store the top x% nodes for each graph
top_x_percent_nodes = {i: {} for i in range(4)}

# Calculate the top x% nodes for each graph and each percentage from 0 to 30
percentages = list(range(0, 11))  # From 0% to 30%
for i in range(4):
    for x in percentages:
        top_x_percent_nodes[i][x] = get_top_x_percent_nodes(top_30_embeddings[i], x)

# Dictionary to store the percentage overlap for each graph with graph 3
overlap_percent_with_3 = {i: [] for i in range(3)}

# Calculate the percentage overlap
for x in percentages:
    for i in range(3):  # Graphs 0, 1, and 2
        overlap_percent = calculate_overlap_percent(top_x_percent_nodes[i][x], top_x_percent_nodes[3][x])
        overlap_percent_with_3[i].append(overlap_percent)

# Define colorblind-friendly colors and graph names
colorblind_friendly_colors = ['darkorange', 'dodgerblue', 'seagreen']
graph_names = [
    "AD + Type 2 Diabetes + Hypertension",
    "AD + Hypertension",
    "AD + Diabetes",
    "AD only"
]

# Plot the percentage overlap with colorblind-friendly colors and renamed lines
plt.figure(figsize=(12, 8))
for i in range(3):
    plt.plot(percentages, overlap_percent_with_3[i], label=graph_names[i], color=colorblind_friendly_colors[i])
plt.xlabel('Top x% Nodes')
plt.ylabel('Percentage Overlap with AD only')
plt.title('Percentage Overlap of Top x% Nodes with AD only')
plt.legend()
plt.grid(True)
plt.show()
