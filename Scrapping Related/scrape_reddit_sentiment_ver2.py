import praw
import logging
import pandas as pd
from tqdm import tqdm
import nltk
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure you have downloaded the necessary NLTK data files
nltk.download('punkt')
nltk.download('vader_lexicon')

# Reddit API credentials (replace with your own credentials)
reddit = praw.Reddit(
    client_id='LmoF1XOmk2ejtYc-4mcevg',
    client_secret='LBebw5DAtL4K7-UaaZlKab2za9Uq3Q',
    user_agent='script:airdrop_scam_detector:v1.0 (by u/JJSIM98)'  # A descriptive user agent string
)

# List of common search queries
search_queries = ['airdrop scam', 'crypto scam', 'blockchain scam', 'ICO scam', 'NFT scam']

# Function to process comments and their replies
def process_comments(comment, search_query, submission_title):
    comments_data = []
    comments_data.append({
        'Search_Query': search_query,
        'Title': submission_title,
        'Author': comment.author.name if comment.author else 'N/A',
        'Created_UTC': comment.created_utc,
        'Upvotes': comment.score,
        'Comment': comment.body,
        'Comment_Author': comment.author.name if comment.author else 'N/A',
        'Comment_Upvotes': comment.score,
        'Sentiment': 'N/A',  # Placeholder for sentiment analysis
        'Scam_Potential': 'N/A'  # Placeholder for scam potential
    })

    # Process replies
    if hasattr(comment, 'replies'):
        for reply in comment.replies:
            comments_data.extend(process_comments(reply, search_query, submission_title))
    
    return comments_data

# Function to process submissions
def process_submission(submission, search_query):
    submission.comments.replace_more(limit=5)
    comments = submission.comments.list()[:20]  # Limit to first 20 comments
    for comment in comments:
        submission_data.extend(process_comments(comment, search_query, submission.title))

# Analyzing and saving the submissions
submission_data = []

# Iterate over each search query
for search_query in search_queries:
    logging.info(f"Searching for: {search_query}")
    submissions = reddit.subreddit('all').search(search_query, limit=50)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for submission in tqdm(submissions, desc=f"Processing submissions for query: {search_query}"):
            executor.submit(process_submission, submission, search_query)

# Convert to DataFrame
df = pd.DataFrame(submission_data)

# Save to CSV
csv_filename = 'reddit_scam_data.csv'
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
