import praw
import prawcore
import logging
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Reddit API credentials (replace with your own credentials)
reddit = praw.Reddit(
    client_id='LmoF1XOmk2ejtYc-4mcevg',
    client_secret='LBebw5DAtL4K7-UaaZlKab2za9Uq3Q',
    user_agent='script:airdrop_scam_detector:v1.0 (by u/JJSIM98)'  # A descriptive user agent string
)

# Load the list of airdrop names with no counts
no_count_airdrops = pd.read_csv('airdrop_sentiment_zero_total.csv')['airdrop_name'].tolist()

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

# Analyzing and saving the submissions
submission_data = []
max_comments = 100  # Increased limit to ensure more data

# Iterate over each airdrop name with no counts
for airdrop_name in no_count_airdrops:
    search_query = f'"{airdrop_name}"'  # Direct search for the airdrop name
    
    total_comments = 0
    if total_comments >= max_comments:
        break
        
    logging.info(f"Searching for: {search_query}")
    submissions = search_reddit(search_query, limit=30)  # Increased limit to ensure more data
        
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
csv_filename = 'new_reddit_airdrop_data_version3.csv'
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
