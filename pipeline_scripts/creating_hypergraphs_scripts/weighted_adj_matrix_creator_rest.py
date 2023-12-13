import pandas as pd
from collections import defaultdict
from scipy.sparse import csr_matrix, lil_matrix
import scipy.sparse
from tqdm import tqdm

# Function to parse paths
def parse_path(path):
    nodes = path.split("–")
    return nodes[1:-1]  # Exclude the end nodes

# List of input files
inputs = [
    ["/Biological_Paths_4750.csv",
    "/Biological_Paths_Above_90_17287.csv",
    "/Biological_Paths_Above_90_38409.csv"], 
    [
    "/Biological_Paths_4750.csv",
    "/Biological_Paths_Above_90_17287.csv"
    ], 
    [
    "/Biological_Paths_Above_90_17287.csv",
    "/Biological_Paths_Above_90_38409.csv"
    ], 
    [
    "/Biological_Paths_Above_90_17287.csv"
    ]
]

#index of the input that you want to create. 
number = 0
# Combine all input files into one DataFrame
all_dfs = [pd.read_csv(input_file) for input_file in inputs[number]]
combined_df = pd.concat(all_dfs).reset_index(drop=True)

# Parse paths and filter out two-node paths
combined_df["nodes"] = combined_df["path"].apply(parse_path)
combined_df = combined_df[combined_df["nodes"].apply(len) > 0]

# Reset index for the combined DataFrame
combined_df = combined_df.reset_index()

# Save the index-to-path mapping
combined_df[['index', 'path']].to_csv("/for_paper/{}_index_to_path.csv".format(number), index=False)

# Create node-to-indices dictionary
node_to_indices = defaultdict(set)
for index, row in tqdm(combined_df.iterrows()):
    for node in row['nodes']:
        node_to_indices[node].add(index)

# Initialize and populate adjacency matrix
N = len(combined_df)
adj_matrix = lil_matrix((N, N), dtype=int)
for indices in tqdm(node_to_indices.values()):
    for i in indices:
        for j in indices:
            if i != j:
                adj_matrix[i, j] += 1

# Convert to CSR and normalize
adj_matrix = adj_matrix.tocsr()
adj_matrix.data = adj_matrix.data / adj_matrix.data.max()

# Save the CSR matrix
scipy.sparse.save_npz("/for_paper/{}_weighted_adj_matrix.npz".format(number), adj_matrix)
