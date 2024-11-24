import pandas as pd

# Load the datasets with utf-8-sig encoding
file_path_latest = 'airdrops_data_latest_ITP1.csv'
file_path_airdrops = 'airdrops_data_latest.csv'

# Read the CSV files using utf-8-sig encoding
data_latest = pd.read_csv(file_path_latest, encoding='utf-8-sig')
data_airdrops = pd.read_csv(file_path_airdrops, encoding='utf-8-sig')

# Find titles that are in 'airdrops_data_latest.csv' but not in 'airdrops_data_latest_ITP1.csv'
titles_airdrops = data_airdrops['Title']
titles_latest = data_latest['Title']

# Filter rows from 'airdrops_data_latest.csv' where the title does not exist in 'airdrops_data_latest_ITP1.csv'
unique_to_airdrops = data_airdrops[~titles_airdrops.isin(titles_latest)]

# Save the filtered data to a new CSV file with utf-8-sig encoding and NaN values preserved
output_unique_titles_file = 'testing_airdrops_data.csv'
unique_to_airdrops.to_csv(output_unique_titles_file, index=False, encoding='utf-8-sig', na_rep='n/a')
