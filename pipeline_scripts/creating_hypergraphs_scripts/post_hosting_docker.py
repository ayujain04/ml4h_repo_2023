from neo4j import GraphDatabase
import pandas as pd
from tqdm import tqdm

# Initialize the Neo4j driver
driver = GraphDatabase.driver("bolt://localhost:7687")

def execute_query(query):
    # Start a new session
    with driver.session() as session:
        # Execute the query
        result = session.run(query)
        # Return the result
        return result.data()

folders= []

inputs = [
]

outputs = []


for folder, input, output in tqdm(zip(folders, inputs, outputs)):
    # Read the CSV file
    df = pd.read_csv(input)

    # Create an empty DataFrame to hold the results
    results_df = pd.DataFrame()

    # Execute each query in the CSV file
    for query in tqdm(df.iloc[:, 0]):
        # Try to execute the query
        result = execute_query(query)
        # Convert the result to a DataFrame and append it to the results_df
        results_df = pd.concat([results_df, pd.DataFrame(result)])

    # Save the results to a CSV file
    results_df.to_csv(folder + output, index=False)
