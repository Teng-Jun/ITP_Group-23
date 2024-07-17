import requests
import pandas as pd
from tqdm import tqdm
import os
import time

# Define the base directory
base_dir = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related'

# Load the CSV file with the coins you want to fetch images for
csv_file = os.path.join(base_dir, 'JJreddit1stpart_scraped_data_csv', 'matched_coins_with_details_reddit_ver7.csv')
coins_df = pd.read_csv(csv_file)

# Function to fetch coin details, including the image, with exponential backoff
def fetch_coin_details(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    retries = 5
    backoff_time = 1  # start with 1 second
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            coin_data = response.json()
            image_url = coin_data.get('image', {}).get('thumb', '')
            return image_url
        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for {coin_id}: {e}")
            if response.status_code == 429:  # HTTP status code for Too Many Requests
                print(f"Rate limit hit, sleeping for {backoff_time} seconds...")
                time.sleep(backoff_time)
                backoff_time *= 2  # double the wait time for the next retry
            else:
                break
    return ''

# Adding a new column for the image URLs
coins_df['image'] = ''

# Fetching the image URL for each coin in the CSV
for index, row in tqdm(coins_df.iterrows(), total=coins_df.shape[0], desc='Fetching coin images'):
    coin_id = row['id']
    image_url = fetch_coin_details(coin_id)
    coins_df.at[index, 'image'] = image_url
    # To avoid hitting rate limits too frequently, add a short sleep after each request
    time.sleep(0.1)

# Save the list of coins with images to a new CSV file
output_file = os.path.join(base_dir, 'JJreddit1stpart_scraped_data_csv', 'coingecko_matched_coins_with_images.csv')
coins_df.to_csv(output_file, index=False)

print(f"Coin data with images saved to '{output_file}'")
