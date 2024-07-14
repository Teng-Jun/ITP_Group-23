import pandas as pd

# Load existing and new data
existing_data = pd.read_csv('reddit_airdrop_data.csv', encoding='ISO-8859-1')
new_data = pd.read_csv('new_reddit_airdrop_data_version2.csv')

# Combine the data
combined_data = pd.concat([existing_data, new_data])

# Save combined data to CSV
combined_data.to_csv('combined_reddit_airdrop_data_version2.csv', index=False)
