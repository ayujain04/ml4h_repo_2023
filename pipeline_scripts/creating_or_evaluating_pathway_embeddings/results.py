import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def share_nodes_ignore_last(path1, path2):
    nodes1 = set(path1.split('–')[:-1])
    nodes2 = set(path2.split('–')[:-1])
    return 'no' if nodes1.isdisjoint(nodes2) else 'yes'

def get_closest_nodes_ignore_last(node_name, node_embeddings, index_to_path_df):
    filtered_df = index_to_path_df[index_to_path_df["path"] == node_name]
    
    if filtered_df.empty:
        print(f"Warning: Node '{node_name}' not found.")
        return None
    
    node_index = filtered_df.index[0]
    node_embedding = node_embeddings[node_index]
    cosine_similarities = cosine_similarity([node_embedding], node_embeddings).flatten()
    
    top_indices = np.argsort(-cosine_similarities)
    closest_nodes = index_to_path_df.loc[top_indices, "path"].tolist()
    closest_nodes_similarities = cosine_similarities[top_indices]
    obvious_values = [share_nodes_ignore_last(node_name, path) for path in closest_nodes]

    results_df = pd.DataFrame({
        "Queried Node": node_name,
        "Closest Node": closest_nodes,
        "Cosine Similarity": closest_nodes_similarities,
        "Obvious": obvious_values
    })
    return results_df

# File paths
embedding_files = [
    '/0_weighted_adj_matrix_embeddings.npy',
    '/1_weighted_adj_matrix_embeddings.npy',
    '/2_weighted_adj_matrix_embeddings.npy',
    '/3_weighted_adj_matrix_embeddings.npy'
]

index_to_path_files = [
    '/0_index_to_path.csv',
    '/1_index_to_path.csv',
    '/2_index_to_path.csv',
    '/3_index_to_path.csv'
]

# Paths
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

# Initialize master DataFrames for each embedding file
for emb_file, idx_file in zip(embedding_files, index_to_path_files):
    node_embeddings = np.load(emb_file)
    index_to_path_df = pd.read_csv(idx_file)
    
    master_df = pd.DataFrame()
    
    for path in paths:
        closest_nodes_df = get_closest_nodes_ignore_last(path, node_embeddings, index_to_path_df)
        
        if closest_nodes_df is not None:
            # Remove rows where Queried Node and Closest Node are the same
            closest_nodes_df = closest_nodes_df[closest_nodes_df['Queried Node'] != closest_nodes_df['Closest Node']]
            
            master_df = pd.concat([master_df, closest_nodes_df], ignore_index=True)

    top_30_percentile = np.percentile(master_df['Cosine Similarity'], 70)
    master_df_top_30 = master_df[master_df['Cosine Similarity'] >= top_30_percentile]
    
    output_csv = f"combined_top_30_for_{emb_file.split('/')[-1].split('.')[0]}.csv"
    master_df_top_30.to_csv(output_csv, index=False)
