import pandas as pd

# Load the sentiment results with specified encoding
sentiment_results = pd.read_csv('airdrop_sentiment_results.csv', encoding='ISO-8859-1')

# Identify airdrop names with zero counts
no_count_airdrops = sentiment_results[(sentiment_results['positive'] == 0) & 
                                      (sentiment_results['neutral'] == 0) & 
                                      (sentiment_results['negative'] == 0)]['airdrop_name'].tolist()

# Save the list of airdrop names with no counts to a new CSV file for reference
no_count_airdrops_df = pd.DataFrame(no_count_airdrops, columns=['airdrop_name'])
no_count_airdrops_df.to_csv('no_count_airdrops.csv', index=False)

no_count_airdrops
