import pandas as pd

# Function to load CSV file with different encodings
def load_csv_with_encoding(filepath):
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode the file with available encodings")

# Load the old and new CSV files
old_csv_path = 'new_airdrop_sentiment_results_version3.csv'
new_csv_path = 'new_airdrop_sentiment_results_updated_1.csv'

old_df = load_csv_with_encoding(old_csv_path)
new_df = load_csv_with_encoding(new_csv_path)

# Filter rows in the old CSV where 'total' is more than 0
old_df_filtered = old_df[old_df['total'] > 0]

# Find rows in the old CSV where 'total' is 0 and in the new CSV
old_with_zero_total = old_df[old_df['total'] == 0]
new_in_old_with_zero_total = new_df[new_df['airdrop_name'].isin(old_with_zero_total['airdrop_name'])]

# Rows to be kept from the new CSV (those that don't exist in the old CSV)
new_unique = new_df[~new_df['airdrop_name'].isin(old_df['airdrop_name'])]

# Combine the filtered old rows and new rows
combined_df = pd.concat([old_df_filtered, new_in_old_with_zero_total, new_unique]).drop_duplicates(subset=['airdrop_name']).reset_index(drop=True)

# Save the combined dataframe to a new CSV file
combined_csv_path = 'combined_airdrop_sentiment_results_2.csv'
combined_df.to_csv(combined_csv_path, index=False)

print(f"Combined CSV saved at: {combined_csv_path}")
