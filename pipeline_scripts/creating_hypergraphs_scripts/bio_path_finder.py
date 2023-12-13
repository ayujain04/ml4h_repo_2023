import pandas as pd
import re
import os

# List of file paths to process
file_paths = [
    '/output_38409.csv',
    '/output_4750.csv',
    '/output_17287.csv'
]

# Function to process each file
def process_file(file_path):
    # Load the original DataFrame
    df = pd.read_csv(file_path)

    # Extract unique elements from the 'path' column
    unique_elements = set()
    for path in df['path']:
        elements = re.split(r'\W+', path)
        unique_elements.update(elements)
    
    # Load the Gene Nodes DataFrame and convert the 'name' column to uppercase
    df_gene_nodes = pd.read_csv('Gene_Nodes.csv')
    df_gene_nodes['name'] = df_gene_nodes['name'].str.upper()

    # Create a set of names from the Gene Nodes DataFrame
    gene_names_set = set(df_gene_nodes['name'])

    # Identify biological elements
    biological_elements = unique_elements.intersection(gene_names_set)
    
    # Function to check if a path is biological
    def is_biological_path(path):
        elements = re.split(r'\W+', path)
        return any(element in biological_elements for element in elements)
    
    # Filter the DataFrame to include only biological paths
    df_biological_paths = df[df['path'].apply(is_biological_path)]
    
    # Create output file name based on the input file name
    file_num = re.search(r'_(\d+)', file_path).group(1)
    output_file_name = f'/Biological_Paths_{file_num}.csv'
    
    # Save the filtered DataFrame
    df_biological_paths.to_csv(output_file_name, index=False)
    print(f"Processed {file_path}. Output saved as {output_file_name}.")

# Loop through the list of file paths and process each one
for file_path in file_paths:
    process_file(file_path)
