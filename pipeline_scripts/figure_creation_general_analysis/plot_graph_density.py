
import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

# Load the adjacency matrices from the npz files
file_paths = [
    '0_weighted_adj_matrix.npz',
    '1_weighted_adj_matrix.npz',
    '2_weighted_adj_matrix.npz',
    '3_weighted_adj_matrix.npz'
]

# Dictionary to store adjacency matrices
adj_matrices_csr = {}

# Load each file and store the adjacency matrix
for i, file_path in enumerate(file_paths):
    npz_file = np.load(file_path)
    adj_matrices_csr[i] = csr_matrix((npz_file['data'], npz_file['indices'], npz_file['indptr']), shape=npz_file['shape'])

# List to store the graph density for each graph
graph_densities = []

# Calculate the graph density for each adjacency matrix
for i in range(len(adj_matrices_csr)):
    num_nodes = adj_matrices_csr[i].shape[0]
    num_edges = adj_matrices_csr[i].nnz // 2  # Each edge is counted twice in the adjacency matrix
    graph_density = (2 * num_edges) / (num_nodes * (num_nodes - 1))
    graph_densities.append(graph_density)

# Graph names
graph_names = [
    "AD + Type 2 Diabetes + Hypertension",
    "AD + Hypertension",
    "AD + Diabetes",
    "AD only"
]

# Plot the graph densities
plt.figure(figsize=(10, 6))
plt.barh(graph_names, graph_densities, color='lightblue')
plt.xlabel('Graph Density')
plt.title('Graph Density for Different Conditions')
for i, v in enumerate(graph_densities):
    plt.text(v, i, f"{v:.6f}", va='center', ha='left')
plt.show()
