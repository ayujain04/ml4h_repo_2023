import requests
from tqdm import tqdm
import pandas as pd

# Load the CSV file
data = pd.read_csv("id_for_drug_disease_side_effect.csv")

# Filter for rows where the type is 'Compound'
compounds = data[data['type'] == 'Compound']

# The target_id: first is Parkinson's, ALS, VD, hypertension, CHD
#targets = [3969, 16507, 29220, 31080, 4750, 36742, 30073, 1105, 16770, 25017, 22725, 16145]
targets = [41316, 8315, 31624, 38409, 34277, 29603, 17820, 15393]
# Iterate through each target
for target_id in targets:
    # The list to store the cypher_query values for each target
    cypher_queries = []

    # Iterate through each row in the filtered data
    for _, row in tqdm(compounds.iterrows()):
        # The source_id
        source_id = row['id']

        # Make the API call
        response = requests.get(f"https://search-api.het.io/v1/metapaths/source/{source_id}/target/{target_id}/")

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_response = response.json()

            # Get the cypher_query from each path_counts and append them to the list
            for path_counts in json_response['path_counts']:
                cypher_queries.append(path_counts['cypher_query'])

    # Convert the list of cypher_query values to a DataFrame
    df = pd.DataFrame(cypher_queries, columns=['cypher_query'])

    # Save the DataFrame to a CSV file
    file_name = f"rest_cypher_target_{target_id}.csv"  # Use a dynamic file name
    df.to_csv(file_name, index=False)
