import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load the node embeddings
node_embeddings = np.load("/weighted_adj_matrix_based_on_shared_node_number/node_embeddings_weighted_walk.npy")
# Load the index-to-path mapping
index_to_path_df = pd.read_csv("/weighted_adj_matrix_based_on_shared_node_number/AD_path_to_index.csv")

# Function to check if two paths share any nodes, ignoring the last node
def share_nodes_ignore_last(path1, path2):
    # Assume that the nodes in a path are separated by '–'
    nodes1 = set(path1.split('–')[:-1])
    nodes2 = set(path2.split('–')[:-1])
    
    # If the intersection of the node sets is empty, return "no", else return "yes"
    return 'no' if nodes1.isdisjoint(nodes2) else 'yes'

def get_closest_nodes_ignore_last(node_name, percentile=10):
    # Get the index of the queried node
    node_index = index_to_path_df[index_to_path_df["path"] == node_name].index[0]
    
    # Get the embedding of the queried node
    node_embedding = node_embeddings[node_index]
    
    # Compute cosine similarity with all nodes
    cosine_similarities = cosine_similarity([node_embedding], node_embeddings).flatten()
    
    # Calculate the threshold for the top percentile
    threshold = np.percentile(cosine_similarities, 100-percentile)
    
    # Get the indices of the top percentile closest nodes
    top_indices = np.where(cosine_similarities >= threshold)[0]
    
    # Get the corresponding node names and cosine similarity values
    closest_nodes = index_to_path_df.loc[top_indices, "path"].tolist()
    closest_nodes_similarities = cosine_similarities[top_indices]
    
    # Check if the paths share any nodes with the queried path, ignoring the last node
    obvious_values = [share_nodes_ignore_last(node_name, path) for path in closest_nodes]
    
    # Combine the results into a DataFrame
    results_df = pd.DataFrame({
        "Queried Node": node_name,
        "Closest Node": closest_nodes,
        "Cosine Similarity": closest_nodes_similarities,
        "Obvious": obvious_values
    })
    
    return results_df

# Full list of paths
# Full list of paths
# Full list of paths
# Full list of paths
# Define the paths as an array of strings
# Creating an array of strings
# Splitting each line by the delimiter '–' and storing each line as a list in an array
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

# Splitting the raw data by lines and storing it in a list
paths = data_raw.strip().split("\n")





# Generate the CSV filenames
csv_file_names = ["AD_" + path.replace("–", "_").replace(" ", "_").replace("'", "") + ".csv" for path in paths]
csv_file_names


for path,output in zip(paths, csv_file_names): 
    # Test the function
    # Query node

    # Get the closest nodes
    closest_nodes_df_ignore_last = get_closest_nodes_ignore_last(path)

    # Save the results to a CSV file
    closest_nodes_df_ignore_last.to_csv("/{}".format(output), index=False)

    # Return the first few rows of the results
    closest_nodes_df_ignore_last.head()


'''
methotrexate_vs_world.csv	
Methotrexate–SLC19A1–PAXIP1–Alzheimer's disease
Methotrexate–ABCC10–Parkinson's disease–Alzheimer's disease
Methotrexate–BDH2–Alzheimer's disease
Methotrexate–Pemetrexed–DCK–Alzheimer's disease
Methotrexate–multiple sclerosis–amyotrophic lateral sclerosis–Alzheimer's disease
Methotrexate–SLC19A1–COL18A1–Alzheimer's disease
Methotrexate–GTF2A2–Ropinirole–Alzheimer's disease
Methotrexate–EIF5–amyotrophic lateral sclerosis–Alzheimer's disease
Methotrexate–UBQLN2–Ropinirole–Alzheimer's disease
Methotrexate–NPDC1–CAMTA1–Alzheimer's disease
Methotrexate–HSD17B10–Alzheimer's disease
Methotrexate–MTHFR–Alzheimer's disease

hydroxychloroquine_vs_world.csv	
Hydrochlorothiazide–ABL1–Alzheimer's disease
Hydrochlorothiazide–WRB–Rivastigmine–Alzheimer's disease
Hydrochlorothiazide–ABL1–Parkinson's disease–Alzheimer's disease
Hydrochlorothiazide–WIF1–amyotrophic lateral sclerosis–Alzheimer's disease
Hydrochlorothiazide–CA4–Alzheimer's disease
Hydrochlorothiazide–RRP1B–Parkinson's disease–Alzheimer's disease
Hydrochlorothiazide–SLC22A6–HMOX1–Alzheimer's disease
Hydrochlorothiazide–TBX2–CCDC85B–Alzheimer's disease
Hydrochlorothiazide–ABCF3–Alzheimer's disease
Hydrochlorothiazide–GDF15–Memantine–Alzheimer's disease
Hydrochlorothiazide–CA12–ACAA1–Alzheimer's disease
Hydrochlorothiazide–Trichlormethiazide–SERPINA3–Alzheimer's disease
Hydrochlorothiazide–Trichlormethiazide–PIN1–Alzheimer's disease
Hydrochlorothiazide–Hydroflumethiazide–BDH1–Alzheimer's disease
Hydrochlorothiazide–CA12–APOE–Alzheimer's disease
Hydrochlorothiazide–hypertension–ACAP1–Alzheimer's disease
Hydrochlorothiazide–hypertension–CLU–Alzheimer's disease
Hydrochlorothiazide–hypertension–CHCHD7–Alzheimer's disease
Hydrochlorothiazide–SLC22A6–APP–Alzheimer's disease

rivastigmine_vs_world.csv
Rivastigmine–Parkinson's disease–Alzheimer's disease
Rivastigmine–Parkinson's disease–Memantine–Alzheimer's disease
Rivastigmine–CCNH–Parkinson's disease–Alzheimer's disease
Rivastigmine–Parkinson's disease–amyotrophic lateral sclerosis–Alzheimer's disease
Rivastigmine–UBQLN2–amyotrophic lateral sclerosis–Alzheimer's disease
Rivastigmine–UBQLN2–amyotrophic lateral sclerosis–Alzheimer's disease
Rivastigmine–Neostigmine–CD320–Alzheimer's disease
Rivastigmine–UBQLN2–Ropinirole–Alzheimer's disease
Rivastigmine–CYP2D6–CCKBR–Alzheimer's disease
Rivastigmine–GHR–Ropinirole–Alzheimer's disease
Rivastigmine–Neostigmine–ABCB1–Alzheimer's disease
Rivastigmine–CYP2D6–Parkinson's disease–Alzheimer's disease
Rivastigmine–GDPD5–CYP46A1–Alzheimer's disease
Rivastigmine–Parkinson's disease–CNGB1–Alzheimer's disease
Rivastigmine–ACHE–APP–Alzheimer's disease
Rivastigmine–CDC20–Donepezil–Alzheimer's disease

memantine_vs_world.csv		
Memantine–Parkinson's disease–Alzheimer's disease
Memantine–CYTH1–Alzheimer's disease
Memantine–Parkinson's disease–Rivastigmine–Alzheimer's disease
Memantine–Parkinson's disease–amyotrophic lateral sclerosis–Alzheimer's disease
Memantine–TIPARP–amyotrophic lateral sclerosis–Alzheimer's disease
Memantine–GRIN2B–Alzheimer's disease
Memantine–GRIN1–DESI2–Alzheimer's disease
Memantine–NFKBIA–B4GAT1–Alzheimer's disease
Memantine–GRIN1–PTK2B–Alzheimer's disease
Memantine–GDF15–brain–Alzheimer's disease
Memantine–Parkinson's disease–CNGB1–Alzheimer's disease
Memantine–GRIN3A–DDAH1–Alzheimer's disease

sulfasalazine_vs_world.csv

Sulfasalazine–TBXAS1–Parkinson's disease–Alzheimer's disease
Sulfasalazine–PTGS2–Alzheimer's disease
Sulfasalazine–UBQLN2–amyotrophic lateral sclerosis–Alzheimer's disease
Sulfasalazine–UBQLN2–amyotrophic lateral sclerosis–Alzheimer's disease
Sulfasalazine–UBQLN2–Rivastigmine–Alzheimer's disease
Sulfasalazine–GDF15–Memantine–Alzheimer's disease
Sulfasalazine–PPARG–CD33–Alzheimer's disease
Sulfasalazine–CHUK–DDX17–Alzheimer's disease
Sulfasalazine–UBQLN2–Ropinirole–Alzheimer's disease
Sulfasalazine–PTGS2–amyotrophic lateral sclerosis–Alzheimer's disease
Sulfasalazine–ABCC2–Alzheimer's disease
Sulfasalazine–TP53BP2–telencephalon–Alzheimer's disease
Sulfasalazine–Vismodegib–ABCB1–Alzheimer's disease
Sulfasalazine–PTGS2–telencephalon–Alzheimer's disease
Sulfasalazine–PTGS2–amyotrophic lateral sclerosis–Alzheimer's disease
Sulfasalazine–GDF15–brain–Alzheimer's disease
Sulfasalazine–TP53BP2–APP–Alzheimer's disease
Sulfasalazine–rheumatoid arthritis–Prodromal Symptoms–Alzheimer's disease
'''