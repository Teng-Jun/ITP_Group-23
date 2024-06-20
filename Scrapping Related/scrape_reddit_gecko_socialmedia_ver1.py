import pandas as pd
import requests
from tqdm import tqdm
import time

# Load the matched coins data with URLs
matched_coins_df = pd.read_csv('matched_coins_reddit_ver4.csv')

# Function to fetch coin details from CoinGecko with retry mechanism
def fetch_coin_details(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    max_retries = 5
    retry_delay = 10  # seconds

    for attempt in range(max_retries):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:  # Rate limit exceeded
            print(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print(f"Error fetching details for {coin_id}: {response.status_code}")
            break
    return None

# Initialize empty lists to store the results
official_websites = []
social_media_links = []

# Fetch details for each matched coin
for _, row in tqdm(matched_coins_df.iterrows(), total=matched_coins_df.shape[0], desc="Fetching coin details"):
    coin_id = row['id']
    details = fetch_coin_details(coin_id)
    
    if details:
        # Get official website
        official_website = details['links']['homepage'][0] if details['links']['homepage'] else ''
        official_websites.append(official_website)
        
        # Get social media links (e.g., Twitter)
        twitter_url = details['links']['twitter_screen_name'] if 'twitter_screen_name' in details['links'] else ''
        facebook_url = details['links']['facebook_username'] if 'facebook_username' in details['links'] else ''
        reddit_url = details['links']['subreddit_url'] if 'subreddit_url' in details['links'] else ''
        
        social_media = {
            'Twitter': twitter_url,
            'Facebook': facebook_url,
            'Reddit': reddit_url
        }
        social_media_links.append(social_media)
    else:
        official_websites.append('')
        social_media_links.append({'Twitter': '', 'Facebook': '', 'Reddit': ''})

    # Sleep for a short time to respect the rate limit
    time.sleep(1)

# Add the fetched data to the DataFrame
matched_coins_df['Official_Website'] = official_websites
matched_coins_df['Social_Media'] = social_media_links

# Save the updated DataFrame to a new CSV file
updated_csv_filename = 'matched_coins_with_details_reddit_ver4.csv'
matched_coins_df.to_csv(updated_csv_filename, index=False)

print(f"Updated matched coins data with details saved to {updated_csv_filename}")
