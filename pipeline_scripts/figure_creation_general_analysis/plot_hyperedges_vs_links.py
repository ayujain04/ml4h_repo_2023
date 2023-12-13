
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

# Lists to store the number of nodes and connections for each graph
num_nodes_list = []
num_connections_list = []

# Extract the number of nodes and connections from each adjacency matrix
for i in range(len(adj_matrices_csr)):
    num_nodes = adj_matrices_csr[i].shape[0]
    num_connections = adj_matrices_csr[i].nnz  # Number of non-zero elements
    num_nodes_list.append(num_nodes)
    num_connections_list.append(num_connections)

# Rename the graphs based on the given conditions
graph_names = [
    "AD + Type 2 Diabetes + Hypertension",
    "AD + Hypertension",
    "AD + Diabetes",
    "AD only"
]

# Plot the number of hyperedges vs. the number of links
plt.figure(figsize=(12, 8))
plt.scatter(num_nodes_list, num_connections_list, c='blue', marker='o', s=100)
plt.xlabel("Number of Hyperedges")
plt.ylabel("Number of Links")
plt.yticks(range(0, max(num_connections_list) + 1, 1000000))
for i, (num_nodes, num_connections) in enumerate(zip(num_nodes_list, num_connections_list)):
    plt.annotate(graph_names[i], (num_nodes, num_connections), textcoords="offset points", xytext=(0, 10), ha='center')
plt.show()
