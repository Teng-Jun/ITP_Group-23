import praw
import prawcore
import logging
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import random
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials (replace with your own credentials)
reddit = praw.Reddit(
    client_id='LmoF1XOmk2ejtYc-4mcevg',
    client_secret='LBebw5DAtL4K7-UaaZlKab2za9Uq3Q',
    user_agent='script:airdrop_scam_detector:v1.0 (by u/JJSIM98)'  # A descriptive user agent string
)

# Function to load CSV file with different encodings
def load_csv_with_encoding(filepath):
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            logging.warning(f"Failed to read {filepath} with {encoding} encoding. Trying next encoding...")
    raise UnicodeDecodeError(f"Unable to read {filepath} with tried encodings.")

# Load the latest airdrop data and sentiment analysis results
latest_airdrops = load_csv_with_encoding(r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\new_airdrops_data_latest.csv')
sentiment_results = load_csv_with_encoding(r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit2ndpart_scapred_data_csv\new_airdrop_sentiment_results_version3.csv')

# Determine which airdrops need to be scraped again
no_count_airdrops = sentiment_results[sentiment_results['total'] == 0]['airdrop_name'].tolist()
new_airdrops = latest_airdrops[~latest_airdrops['Title'].isin(sentiment_results['airdrop_name'])]['Title'].tolist()

# Combine the lists to get a final list of airdrops to scrape
airdrop_names_to_scrape = list(set(no_count_airdrops + new_airdrops))

# Save the list of airdrop names that need to be scraped to a new CSV file
airdrop_names_to_scrape_df = pd.DataFrame(airdrop_names_to_scrape, columns=['airdrop_name'])
airdrop_names_to_scrape_df.to_csv('airdrop_names_to_scrape.csv', index=False)
print(f"List of airdrop names to scrape saved to 'airdrop_names_to_scrape.csv'")

# Function to process comments and their replies
def process_comments(comment, submission):
    comments_data = []
    comments_data.append({
        'Title': submission.title,
        'URL': submission.url,
        'Author': submission.author.name if submission.author else 'N/A',
        'Created_UTC': submission.created_utc,
        'Upvotes': submission.score,
        'Comment': comment.body,
        'Comment_Author': comment.author.name if comment.author else 'N/A',
        'Comment_Upvotes': comment.score
    })

    # Process replies
    if hasattr(comment, 'replies'):
        for reply in comment.replies[:10]:  # Limit to first 10 replies
            comments_data.extend(process_comments(reply, submission))
    
    return comments_data

# Function to process submissions
def process_submission(submission, search_query, max_comments, current_count):
    try:
        submission.comments.replace_more(limit=1)
        comments = submission.comments.list()[:10]  # Limit to first 10 comments
        comments_data = []
        for comment in comments:
            if current_count + len(comments_data) >= max_comments:
                break
            comments_data.extend(process_comments(comment, submission))
        return comments_data
    except Exception as e:
        logging.error(f"Error processing submission {submission.id} for query {search_query}: {e}")
        return []

# Function to search Reddit with rate limit handling
def search_reddit(query, limit):
    while True:
        try:
            return list(reddit.subreddit('all').search(query, limit=limit))
        except prawcore.exceptions.TooManyRequests as e:
            wait_time = int(e.response.headers.get('retry-after', 60)) + random.randint(1, 30)
            logging.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)

# Function to perform the scraping
def perform_scraping(airdrop_names):
    submission_data = []
    max_comments = 100  # Increased limit to ensure more data

    # Iterate over each airdrop name with no counts
    for airdrop_name in airdrop_names:
        search_queries = [f'"{airdrop_name}" cryptocurrency', f'"{airdrop_name}" airdrop', f'{airdrop_name} crypto']
        
        total_comments = 0
        for search_query in search_queries:
            if total_comments >= max_comments:
                break
            
            logging.info(f"Searching for: {search_query}")
            submissions = search_reddit(search_query, limit=10)  # Increased limit to ensure more data
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for submission in tqdm(submissions, desc=f"Processing submissions for query: {search_query}"):
                    futures.append(executor.submit(process_submission, submission, search_query, max_comments, total_comments))

                for future in tqdm(futures, desc="Collecting results"):
                    result = future.result()
                    submission_data.extend(result)
                    total_comments += len(result)
                    print(f"Added {len(result)} comments for query: {search_query}")

                    if total_comments >= max_comments:
                        break

            # Sleep to avoid hitting the rate limit
            time.sleep(1)

    # Convert to DataFrame
    df = pd.DataFrame(submission_data)

    # Save to CSV
    csv_filename = 'new_reddit_airdrop_data_combined.csv'
    df.to_csv(csv_filename, index=False)

    print(f"Data saved to {csv_filename}")

# Perform the scraping after saving the airdrop names
perform_scraping(airdrop_names_to_scrape)

# If you need to load other CSV files in the same directory
def load_other_csv_files(base_dir, csv_filename):
    csv_file = os.path.join(base_dir, csv_filename)
    df = pd.read_csv(csv_file)
    return df

# Example usage
base_dir = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related'
example_df = load_other_csv_files(base_dir, 'JJreddit1stpart_scraped_data_csv/coingecko_matched_coins_with_images_final_retry.csv')
print(example_df.head())
