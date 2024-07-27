import pandas as pd

# Load the combined CSV file
combined_csv_path = 'combined_airdrop_sentiment_results.csv'
combined_df = pd.read_csv(combined_csv_path)

# Filter rows where 'total' is 0
zero_total_df = combined_df[combined_df['total'] == 0]

# Save the filtered rows to a new CSV file
zero_total_csv_path = 'airdrop_sentiment_zero_total.csv'
zero_total_df.to_csv(zero_total_csv_path, index=False)

print(f"CSV file with zero total saved at: {zero_total_csv_path}")
