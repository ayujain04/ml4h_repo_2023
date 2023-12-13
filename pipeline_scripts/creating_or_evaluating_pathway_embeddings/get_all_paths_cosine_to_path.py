import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Function to check if two paths share any nodes, ignoring the last node
def share_nodes_ignore_last(path1, path2):
    nodes1 = set(path1.split('–')[:-1])
    nodes2 = set(path2.split('–')[:-1])
    return 'no' if nodes1.isdisjoint(nodes2) else 'yes'

# Function to get closest nodes ignoring the last node in the path
def get_closest_nodes_ignore_last(node_name, index_to_path_df, node_embeddings):
    node_index = index_to_path_df[index_to_path_df["path"] == node_name].index[0]
    node_embedding = node_embeddings[node_index]
    cosine_similarities = cosine_similarity([node_embedding], node_embeddings).flatten()
    
    all_indices = np.arange(len(cosine_similarities))
    
    closest_nodes = index_to_path_df.loc[all_indices, "path"].tolist()
    closest_nodes_similarities = cosine_similarities[all_indices]
    
    obvious_values = [share_nodes_ignore_last(node_name, path) for path in closest_nodes]
    
    results_df = pd.DataFrame({
        "Queried Node": node_name,
        "Closest Node": closest_nodes,
        "Cosine Similarity": closest_nodes_similarities,
        "Obvious": obvious_values
    })
    
    return results_df

# Your data raw paths (update this as per your actual data)
data_raw = """Galantamine–MYLK–amyotrophic lateral sclerosis–Alzheimer's disease
Galantamine–MBOAT7–BSN–Alzheimer's disease
Galantamine–Morphine–CYP2C8–Alzheimer's disease
Galantamine–Morphine–ABCB1–Alzheimer's disease
Galantamine–CYP2D6–CCKBR–Alzheimer's disease
Galantamine–MYLK–CALM1–Alzheimer's disease
Galantamine–MYLK–SERPINA3–Alzheimer's disease
Donepezil–HRH3–DRD1–Alzheimer's disease
Donepezil–Tetrabenazine–DNAJA3–Alzheimer's disease
Donepezil–NFIL3–DBN1–Alzheimer's disease
Donepezil–ARL4C–RCAN1–Alzheimer's disease
Donepezil–CYP2D6–CCKBR–Alzheimer's disease
Donepezil–Doxazosin–ABCB1–Alzheimer's disease
Donepezil–CCL2–Alzheimer's disease
Donepezil–NFKBIA–B4GAT1–Alzheimer's disease
Donepezil–TP53BP1–BOLA1–Alzheimer's disease
Donepezil–CDC20–Rivastigmine–Alzheimer's disease
Memantine–CYTH1–Alzheimer's disease
Memantine–TIPARP–amyotrophic lateral sclerosis–Alzheimer's disease
Memantine–GRIN2B–Alzheimer's disease
Memantine–GRIN1–DESI2–Alzheimer's disease
Memantine–NFKBIA–B4GAT1–Alzheimer's disease
Memantine–GRIN1–PTK2B–Alzheimer's disease
Memantine–GDF15–brain–Alzheimer's disease
Memantine–Parkinson's disease–CNGB1–Alzheimer's disease
Memantine–GRIN3A–DDAH1–Alzheimer's disease"""

paths = data_raw.strip().split("\n")

# Loop over each dataset (0 to 3) to process them one by one
for i in tqdm(range(4)):
    # Load the node embeddings and index-to-path mapping
    node_embeddings = np.load(f"{i}_weighted_adj_matrix_embeddings.npy")
    index_to_path_df = pd.read_csv(f"{i}_index_to_path.csv")
    
    # List to store all result dataframes
    all_results = []
    
    for path in paths:
        closest_nodes_df_ignore_last = get_closest_nodes_ignore_last(path, index_to_path_df, node_embeddings)
        
        # Append the result dataframe to the list
        all_results.append(closest_nodes_df_ignore_last)
        
    # Concatenate all dataframes and save to a single CSV file
    final_df = pd.concat(all_results)
    
    # Save the results to a CSV file (update the path as per your requirements)
    output_path = f"dataset_{i}_results.csv"
    final_df.to_csv(output_path, index=False)
    
    # Display the first few rows of the results (optional)
    print(f"Results for dataset {i} saved to {output_path}")
