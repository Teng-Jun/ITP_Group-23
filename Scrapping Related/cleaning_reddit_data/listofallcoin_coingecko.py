import requests
import pandas as pd

# Fetching the list of coins from CoinGecko
response = requests.get('https://api.coingecko.com/api/v3/coins/list')
coins = response.json()

# Convert to DataFrame for easier manipulation
coins_df = pd.DataFrame(coins)
print(coins_df.head())

# Save the list of coins to a CSV file for future use
coins_df.to_csv('coingecko_coins_list_ver1', index=False)
