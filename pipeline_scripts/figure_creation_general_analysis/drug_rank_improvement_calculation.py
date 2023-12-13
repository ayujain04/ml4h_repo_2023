
import pandas as pd

def extract_drug(df):
    df['Drug'] = df['Closest Node'].apply(lambda x: x.split('–')[0])
    return df

def calculate_and_save_rank_improvement(file_0_3, file_1_3, file_2_3, output_prefix):
    # Load the merged dataframes
    extracted_0_3 = pd.read_csv(file_0_3)
    extracted_1_3 = pd.read_csv(file_1_3)
    extracted_2_3 = pd.read_csv(file_2_3)
    
    # Extract the first element ("Drug") from the 'Closest Node' for each condition
    extracted_0_3 = extract_drug(extracted_0_3)
    extracted_1_3 = extract_drug(extracted_1_3)
    extracted_2_3 = extract_drug(extracted_2_3)
    
    # Group by the "Drug" and take the highest rank for each group
    grouped_0_3 = extracted_0_3.groupby('Drug')['Rank_0', 'Rank_3'].min().reset_index()
    grouped_1_3 = extracted_1_3.groupby('Drug')['Rank_1', 'Rank_3'].min().reset_index()
    grouped_2_3 = extracted_2_3.groupby('Drug')['Rank_2', 'Rank_3'].min().reset_index()
    
    # Calculate the rank improvement for each "Drug"
    grouped_0_3['Rank_Improvement_0_3'] = grouped_0_3['Rank_3'] - grouped_0_3['Rank_0']
    grouped_1_3['Rank_Improvement_1_3'] = grouped_1_3['Rank_3'] - grouped_1_3['Rank_1']
    grouped_2_3['Rank_Improvement_2_3'] = grouped_2_3['Rank_3'] - grouped_2_3['Rank_2']
    
    # Save the full data of rank improvement drugs to CSV files
    grouped_0_3.sort_values('Rank_Improvement_0_3', ascending=False).to_csv(output_prefix + '_full_drugs_rank_improvement_0_3.csv', index=False)
    grouped_1_3.sort_values('Rank_Improvement_1_3', ascending=False).to_csv(output_prefix + '_full_drugs_rank_improvement_1_3.csv', index=False)
    grouped_2_3.sort_values('Rank_Improvement_2_3', ascending=False).to_csv(output_prefix + '_full_drugs_rank_improvement_2_3.csv', index=False)

# Example usage (you will need to specify the actual paths of your files and output prefix)
calculate_and_save_rank_improvement("merged_0_3.csv", "merged_1_3.csv", "merged_2_3.csv", "output")
