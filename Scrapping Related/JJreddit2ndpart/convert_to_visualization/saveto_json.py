import pandas as pd

# Attempt to read the CSV file with a different encoding
try:
    sentiment_data = pd.read_csv('combined_airdrop_sentiment_results_2.csv', encoding='utf-8')
except UnicodeDecodeError:
    sentiment_data = pd.read_csv('combined_airdrop_sentiment_results_2.csv', encoding='latin1')

# Save to JSON
sentiment_data.to_json('airguard/sentiment_results2.json', orient='records')

print("Sentiment results saved to JSON.")
