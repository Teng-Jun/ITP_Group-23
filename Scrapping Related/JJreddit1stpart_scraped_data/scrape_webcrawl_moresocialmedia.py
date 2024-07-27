import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse

# Function to check if URL is valid
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

# Function to scrape social media links from a coin's webpage
def scrape_social_media(coin_url, retries=5, backoff_factor=1.0):
    # Try both http and https if no scheme is provided
    if not is_valid_url(coin_url):
        print(f"Invalid URL, attempting to add schemes: {coin_url}")
        coin_url = "http://" + coin_url if not coin_url.startswith(("http://", "https://")) else coin_url

    for attempt in range(retries):
        try:
            response = requests.get(coin_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            social_media = {
                'Instagram': '',
                'Telegram': '',
                'Discord': ''
            }
            
            # Example logic to find social media links, adjust selectors based on actual webpage structure
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                if 'instagram.com' in href:
                    social_media['Instagram'] = href
                elif 't.me' in href:
                    social_media['Telegram'] = href
                elif 'discord.com' in href:
                    social_media['Discord'] = href
                    
            return social_media
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error on attempt {attempt + 1} for URL {coin_url}: {e}")
            if response.status_code == 500:
                break  # Skip retries for server errors
            time.sleep(backoff_factor * (2 ** attempt))
        except requests.RequestException as e:
            print(f"Request error on attempt {attempt + 1} for URL {coin_url}: {e}")
            time.sleep(backoff_factor * (2 ** attempt))
    return None

# Load the matched coins data with URLs
matched_coins_df = pd.read_csv('coingecko_matched_coins_with_images_high_res.csv')

# Initialize new columns
matched_coins_df['Instagram'] = ''
matched_coins_df['Telegram'] = ''
matched_coins_df['Discord'] = ''

# Log errors
error_log = []

total_rows = len(matched_coins_df)

# Iterate over each coin in the DataFrame and scrape social media data
for index, row in matched_coins_df.iterrows():
    coin_url = row['Official_Website']  # Assuming 'Official_Website' column exists in your CSV
    social_media_data = scrape_social_media(coin_url)
    
    if social_media_data:
        matched_coins_df.at[index, 'Instagram'] = social_media_data['Instagram']
        matched_coins_df.at[index, 'Telegram'] = social_media_data['Telegram']
        matched_coins_df.at[index, 'Discord'] = social_media_data['Discord']
    else:
        error_log.append({'row': index, 'url': coin_url})

    # Print progress
    print(f"Processed {index + 1}/{total_rows} ({((index + 1) / total_rows) * 100:.2f}%)")
    
    # Save the intermediate result to avoid losing progress
    if index % 10 == 0:  # Save every 10 rows
        intermediate_csv_path = 'matched_coins_with_details_reddit_ver10_partial.csv'
        matched_coins_df.to_csv(intermediate_csv_path, index=False)
        print(f"Intermediate save at row {index + 1}")

# Save the final DataFrame to a new CSV file
final_csv_path = 'matched_coins_with_details_reddit_ver10.csv'
matched_coins_df.to_csv(final_csv_path, index=False)

# Save the error log to a CSV file
error_log_df = pd.DataFrame(error_log)
error_log_path = 'scrape_errors_log.csv'
error_log_df.to_csv(error_log_path, index=False)

print(f"Updated matched coins data with details saved to {final_csv_path}")
print(f"Error log saved to {error_log_path}")
