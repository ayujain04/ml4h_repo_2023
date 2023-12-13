import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Load gene nodes for filtering
gene_nodes_df = pd.read_csv('/path_to_your_Gene_Nodes.csv')
gene_nodes_set = set(gene_nodes_df['Gene_Names'].str.upper())

# Function to extract middle gene nodes from a node string
def extract_filtered_middle_genes(node_str):
    nodes = node_str.split('-')
    middle_nodes = nodes[1:-1]
    return [node for node in middle_nodes if node.upper() in gene_nodes_set]

# Adjusted function to get counts of middle gene nodes from the "path" column of the mapping dataframe
def get_filtered_middle_gene_counts_from_path(mapping_df):
    all_genes = []
    for node_str in mapping_df['path']:
        all_genes.extend(extract_filtered_middle_genes(node_str))
    return Counter([gene.upper() for gene in all_genes])

# Load all index-to-path mapping files
index_to_path_dfs = [
    pd.read_csv('/path_to_your_0_index_to_path.csv'),
    pd.read_csv('/path_to_your_1_index_to_path.csv'),
    pd.read_csv('/path_to_your_2_index_to_path.csv'),
    pd.read_csv('/path_to_your_3_index_to_path.csv')
]

# Calculating the middle gene node counts using the "path" column of the mapping dataframes
middle_gene_node_counts_case_insensitive = [get_filtered_middle_gene_counts_from_path(df) for df in index_to_path_dfs]

# Labels for the graphs
graph_labels = [
    "AD + Type 2 Diabetes + Hypertension",
    "AD + Hypertension",
    "AD + Diabetes",
    "AD only"
]

# Plotting the data
plt.figure(figsize=(18, 14))

for i in range(4):
    plt.subplot(2, 2, i + 1)  # 2x2 grid of subplots
    gene_counts = middle_gene_node_counts_case_insensitive[i]
    if gene_counts:
        sorted_counts = sorted(gene_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        genes, counts = zip(*sorted_counts)
        plt.bar(genes, counts, color='blue')
        plt.xticks(rotation=90)
        plt.title(graph_labels[i])
        plt.xlabel("Gene Names")
        plt.ylabel("Count")
    else:
        plt.text(0.5, 0.5, 'No middle gene nodes found', ha='center', va='center')
        plt.title(graph_labels[i])
        plt.xlabel("Gene Names")
        plt.ylabel("Count")

plt.tight_layout()
plt.savefig("/path_to_save_your_output.pdf", format="pdf", dpi=300)
plt.show()
