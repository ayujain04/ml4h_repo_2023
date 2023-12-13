 
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

# Function to convert a scipy sparse matrix to a NetworkX graph
def sparse_to_networkx(sparse_matrix):
    G = nx.Graph()
    coo = sparse_matrix.tocoo()
    for i, j, w in zip(coo.row, coo.col, coo.data):
        G.add_edge(i, j, weight=w)
    return G

# Load the adjacency matrices from the npz files
file_paths = [
    '../Data/0_weighted_adj_matrix.npz',
    '../Data/1_weighted_adj_matrix.npz',
    '../Data/2_weighted_adj_matrix.npz',
    '../Data/3_weighted_adj_matrix.npz'
]

# Dictionary to store adjacency matrices
adj_matrices_csr = {}

# Load each file and store the adjacency matrix
for i, file_path in enumerate(file_paths):
    npz_file = np.load(file_path)
    adj_matrices_csr[i] = csr_matrix((npz_file['data'], npz_file['indices'], npz_file['indptr']), shape=npz_file['shape'])

# List to store the average clustering coefficient for each graph
clustering_coefficients = []

# Calculate the average clustering coefficient for each adjacency matrix
for i in range(len(adj_matrices_csr)):
    G = sparse_to_networkx(adj_matrices_csr[i])
    avg_clustering = nx.average_clustering(G)
    clustering_coefficients.append(avg_clustering)

# Graph names
graph_names = [
    "AD + Type 2 Diabetes + Hypertension",
    "AD + Hypertension",
    "AD + Diabetes",
    "AD only"
]

# Plot the average clustering coefficients
plt.figure(figsize=(12, 8))
bars = plt.barh(graph_names, clustering_coefficients, color='lightgreen')
plt.xlabel('Average Clustering Coefficient')
plt.title('Average Clustering Coefficient for Different Conditions')

# Add text inside the bars, making sure they are within the plot area
for i, bar in enumerate(bars):
    width = bar.get_width()
    max_width = plt.xlim()[1]  # Get the maximum x-value of the plot area
    padding = max_width * 0.01  # Add some padding within the plot area
    if width + padding < max_width:
        plt.text(width + padding, i, f"{clustering_coefficients[i]:.6f}", va='center', ha='left')
    else:
        plt.text(width - padding, i, f"{clustering_coefficients[i]:.6f}", va='center', ha='right')

plt.show()
