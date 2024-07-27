import pandas as pd
import ast
import requests
import time

# Load the matched coins data with URLs
matched_coins_df = pd.read_csv('coingecko_matched_coins_with_images_high_res.csv')

# Function to fetch coin data from CoinGecko API
def fetch_coin_data(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    for attempt in range(5):  # Try up to 5 times
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Rate limit exceeded
                print(f"Rate limit exceeded. Waiting for 60 seconds (Attempt {attempt + 1}/5).")
                time.sleep(60)
            else:
                print(f"HTTP error occurred: {e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e} (Attempt {attempt + 1}/5).")
            time.sleep(5)  # Wait a bit before retrying
    return None

# Drop duplicate IDs
matched_coins_df.drop_duplicates(subset='id', inplace=True)

# Initialize new columns
matched_coins_df['Instagram'] = ''
matched_coins_df['Telegram'] = ''
matched_coins_df['Discord'] = ''

total_rows = len(matched_coins_df)

# Iterate over each coin in the DataFrame and fetch social media data
for index, row in matched_coins_df.iterrows():
    coin_id = row['id']  # Assuming 'id' column exists in your CSV
    coin_data = fetch_coin_data(coin_id)
    if coin_data:
        social_media = coin_data.get('links', {})
        instagram_username = social_media.get('instagram_username', '')
        telegram_channel_identifier = social_media.get('telegram_channel_identifier', '')
        discord_url = social_media.get('discord', '')
        
        matched_coins_df.at[index, 'Instagram'] = f"https://www.instagram.com/{instagram_username}" if instagram_username else ''
        matched_coins_df.at[index, 'Telegram'] = f"https://t.me/{telegram_channel_identifier}" if telegram_channel_identifier else ''
        matched_coins_df.at[index, 'Discord'] = discord_url

    # Print progress
    print(f"Processed {index + 1}/{total_rows} ({((index + 1) / total_rows) * 100:.2f}%)")

    # Save the intermediate result to avoid losing progress
    if index % 10 == 0:  # Save every 10 rows
        intermediate_csv_path = 'matched_coins_with_details_reddit_ver8_partial.csv'
        matched_coins_df.to_csv(intermediate_csv_path, index=False)
        print(f"Intermediate save at row {index + 1}")

# Save the final DataFrame to a new CSV file
final_csv_path = 'matched_coins_with_details_reddit_ver8.csv'
matched_coins_df.to_csv(final_csv_path, index=False)

print(f"Updated matched coins data with details saved to {final_csv_path}")
