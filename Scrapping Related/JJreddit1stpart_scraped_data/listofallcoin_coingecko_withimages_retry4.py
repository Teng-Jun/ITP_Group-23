import requests
import pandas as pd
from tqdm import tqdm
import os
import time

# Define the base directory
base_dir = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related'

# Load the existing CSV file with coin data and images
csv_file = os.path.join(base_dir, 'JJreddit1stpart_scraped_data_csv', 'coingecko_matched_coins_with_images_final_retry2.csv')
coins_df = pd.read_csv(csv_file)

# Filter rows where the image URL is empty
coins_to_retry = coins_df[coins_df['image'].isna() | (coins_df['image'] == '') | (coins_df['image'] == 'missing_thumb.png')]

print(f"Total coins to retry: {coins_to_retry.shape[0]}")

# Function to fetch coin details, including the image, with increased backoff time
def fetch_coin_details(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    retries = 5
    backoff_time = 2  # start with 2 seconds
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            coin_data = response.json()
            image_url = coin_data.get('image', {}).get('thumb', '')
            if image_url:
                print(f"Image found for {coin_id}: {image_url}")
            else:
                print(f"No image found for {coin_id}")
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

# Fetching the image URL for each coin that needs retrying
for index, row in tqdm(coins_to_retry.iterrows(), total=coins_to_retry.shape[0], desc='Retrying coin images'):
    coin_id = row['id']
    image_url = fetch_coin_details(coin_id)
    if image_url:
        coins_df.at[index, 'image'] = image_url
    # To avoid hitting rate limits too frequently, add a longer sleep after each request
    time.sleep(0.5)

# Save the updated list of coins with images to a new CSV file
output_file = os.path.join(base_dir, 'JJreddit1stpart_scraped_data_csv', 'coingecko_matched_coins_with_images_final_retry3.csv')
coins_df.to_csv(output_file, index=False)

# Save the coins that still don't have images to a separate file
coins_without_images = coins_df[coins_df['image'].isna() | (coins_df['image'] == '') | (coins_df['image'] == 'missing_thumb.png')]
if not coins_without_images.empty:
    output_no_image_file = os.path.join(base_dir, 'JJreddit1stpart_scraped_data_csv', 'coingecko_coins_without_images.csv')
    coins_without_images.to_csv(output_no_image_file, index=False)
    print(f"Coins without images saved to '{output_no_image_file}'")

print(f"Updated coin data with images saved to '{output_file}'")
