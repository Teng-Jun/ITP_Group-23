import os
import pandas as pd
import json
import praw
import prawcore
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time
import random
from collections import Counter
import re
import csv

# Configure logging to both console and file
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create handlers: one for console, one for file
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('script_log.log', mode='w')  # Log file

# Set the level for the handlers
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Error logger to capture critical errors in a separate file
error_logger = logging.getLogger('error_logger')
error_handler = logging.FileHandler('error_log.log', mode='w')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
error_logger.addHandler(error_handler)

# Reddit API credentials (replace with your own credentials)
reddit = praw.Reddit(
    client_id='LmoF1XOmk2ejtYc-4mcevg',
    client_secret='LBebw5DAtL4K7-UaaZlKab2za9Uq3Q',
    user_agent='script:airdrop_scam_detector:v1.0 (by u/JJSIM98)'  # A descriptive user agent string
)

# Utility Functions
def load_csv_with_encoding(filepath):
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            logging.warning(f"Failed to read {filepath} with {encoding} encoding. Trying next encoding...")
    raise UnicodeDecodeError(f"Unable to read {filepath} with tried encodings.")

def preprocess_text(text):
    if pd.isna(text):
        return ''
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation and special characters
    return text

def analyze_sentiment(text, positive_words, neutral_words, negative_words):
    words = preprocess_text(text).split()
    word_counts = Counter(words)
    positive_count = sum(word_counts[word] for word in positive_words if word in word_counts)
    neutral_count = sum(word_counts[word] for word in neutral_words if word in word_counts)
    negative_count = sum(word_counts[word] for word in negative_words if word in word_counts)
    return positive_count, neutral_count, negative_count

# Step 1: Scrape new airdrop data
def scrape_new_airdrop_data():
    latest_airdrops = load_csv_with_encoding('new_airdrops_data_latest.csv')
    sentiment_results = load_csv_with_encoding('combined_airdrop_sentiment_results_2.csv')
    no_count_airdrops = sentiment_results[sentiment_results['total'] == 0]['airdrop_name'].tolist()
    new_airdrops = latest_airdrops[~latest_airdrops['Title'].isin(sentiment_results['airdrop_name'])]['Title'].tolist()
    # Combine and limit to 20 items for demonstration purposes
    airdrop_names_to_scrape = list(set(no_count_airdrops + new_airdrops))
    
    # Sort the list alphabetically for better progress tracking
    airdrop_names_to_scrape.sort()
    return airdrop_names_to_scrape

# Step 2: Scrape Reddit comments for airdrops
def search_reddit(query, limit):
    while True:
        try:
            return list(reddit.subreddit('all').search(query, limit=limit))
        except prawcore.exceptions.TooManyRequests as e:
            wait_time = int(e.response.headers.get('retry-after', 60)) + random.randint(1, 30)
            logging.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
            time.sleep(wait_time)

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
    if hasattr(comment, 'replies'):
        for reply in comment.replies[:10]:  # Limit to first 10 replies
            comments_data.extend(process_comments(reply, submission))
    return comments_data

# Add this missing function
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

def scrape_reddit_comments(airdrop_names_to_scrape):
    submission_data = []
    max_comments = 100  # Increased limit to ensure more data
    for airdrop_name in airdrop_names_to_scrape:
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
            time.sleep(1)  # Sleep to avoid hitting the rate limit
    return submission_data

# Step 3: Perform sentiment analysis
def perform_sentiment_analysis(reddit_data, airdrop_names):
    positive_words = ['good', 'profitable', 'best', 'exciting', 'rewarding', 'beneficial', 'excellent', 'superior',
    'outstanding', 'amazing', 'delightful', 'brilliant', 'successful', 'advantageous', 'productive',
    'fruitful', 'lucrative', 'effective', 'worthwhile', 'constructive', 'valuable', 'enjoyable',
    'satisfying', 'wonderful', 'favorable', 'promising', 'enhancing', 'great', 'impressive',
    'perfect', 'positive', 'thriving', 'booming', 'winning', 'leading', 'innovative', 'pioneering',
    'revolutionary', 'game-changing', 'optimistic', 'glowing', 'acclaimed', 'recommended', 'epic',
    'majestic', 'splendid', 'miraculous', 'superb', 'magnificent']
    neutral_words = ['stable', 'expected', 'normal', 'average', 'standard', 'common', 'regular', 'typical', 'ordinary',
    'usual', 'customary', 'conventional', 'median', 'moderate', 'neutral', 'unchanged', 'constant',
    'steady', 'routine', 'generic', 'uniform', 'balanced', 'fair', 'middle', 'adequate', 'plain',
    'simple', 'basic', 'unremarkable', 'undistinguished', 'standardized', 'normalized', 'unbiased',
    'straightforward', 'practical', 'functional', 'unexceptional', 'undramatic', 'unadorned',
    'unembellished']
    negative_words = [    'bad', 'loss', 'scam', 'risky', 'problematic', 'dangerous', 'poor', 'terrible', 'horrible',
    'dreadful', 'awful', 'troublesome', 'harmful', 'detrimental', 'disastrous', 'perilous',
    'hazardous', 'fatal', 'lethal', 'deadly', 'destructive', 'unfavorable', 'unpleasant', 'unhappy',
    'sad', 'depressing', 'gloomy', 'miserable', 'disappointing', 'insufficient', 'ineffective',
    'faulty', 'flawed', 'deficient', 'inferior', 'substandard', 'damaging', 'corrosive', 'cancerous',
    'toxic', 'vile', 'sinister', 'ominous', 'dire']
    sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0} for airdrop in airdrop_names}
    for index, row in tqdm(reddit_data.iterrows(), total=reddit_data.shape[0], desc="Analyzing sentiment"):
        title = row['Title']
        comment = row['Comment']
        for airdrop in airdrop_names:
            if airdrop.lower() in preprocess_text(title) or airdrop.lower() in preprocess_text(comment):
                title_sentiment = analyze_sentiment(title, positive_words, neutral_words, negative_words)
                comment_sentiment = analyze_sentiment(comment, positive_words, neutral_words, negative_words)
                sentiment_results[airdrop]['positive'] += title_sentiment[0] + comment_sentiment[0]
                sentiment_results[airdrop]['neutral'] += title_sentiment[1] + comment_sentiment[1]
                sentiment_results[airdrop]['negative'] += title_sentiment[2] + comment_sentiment[2]
    # Calculate total counts and percentages
    for airdrop, sentiments in sentiment_results.items():
        total = sentiments['positive'] + sentiments['neutral'] + sentiments['negative']
        sentiments['total'] = total
        if total > 0:
            sentiments['positive_percentage'] = (sentiments['positive'] / total) * 100
            sentiments['neutral_percentage'] = (sentiments['neutral'] / total) * 100
            sentiments['negative_percentage'] = (sentiments['negative'] / total) * 100
        else:
            sentiments['positive_percentage'] = 0
            sentiments['neutral_percentage'] = 0
            sentiments['negative_percentage'] = 0
        
    return sentiment_results

# Step 4: Save results to CSV and JSON
def save_to_csv_and_json(sentiment_results):
    # Save to CSV
    csv_output_file = 'new_airdrop_sentiment_results_version3.csv'
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as csvfile:  # Add encoding='utf-8'
        fieldnames = ['airdrop_name', 'positive', 'neutral', 'negative', 'total', 'positive_percentage', 'neutral_percentage', 'negative_percentage']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for airdrop, sentiments in sentiment_results.items():
            writer.writerow({
                'airdrop_name': airdrop,
                'positive': sentiments['positive'],
                'neutral': sentiments['neutral'],
                'negative': sentiments['negative'],
                'total': sentiments['total'],
                'positive_percentage': sentiments['positive_percentage'],
                'neutral_percentage': sentiments['neutral_percentage'],
                'negative_percentage': sentiments['negative_percentage']
            })

    print(f"Sentiment analysis results saved to {csv_output_file}")

    # Save to JSON
    json_output_file = 'sentiment_results.json'
    with open(json_output_file, 'w', encoding='utf-8') as jsonfile:  # Add encoding='utf-8'
        json.dump(sentiment_results, jsonfile, indent=4)

    print(f"Sentiment analysis results saved to {json_output_file}")
                


# Main function to run all steps
def main():
    try:
         # Step 1: Scrape new airdrop data
        airdrop_names_to_scrape = scrape_new_airdrop_data()
        
        # Step 2: Scrape Reddit comments
        logger.info("Starting to scrape Reddit comments...")
        reddit_data = pd.DataFrame(scrape_reddit_comments(airdrop_names_to_scrape))
        
        # Save intermediate reddit data to CSV
        reddit_data.to_csv('intermediate_reddit_data.csv', index=False)
        logger.info(f"Intermediate Reddit data saved to 'intermediate_reddit_data.csv'")
        
        # Step 3: Perform sentiment analysis
        logger.info("Starting sentiment analysis...")
        sentiment_results = perform_sentiment_analysis(reddit_data, airdrop_names_to_scrape)
        
        # Step 4: Save results to CSV and JSON
        save_to_csv_and_json(sentiment_results)

        logger.info("Process completed successfully.")
        
    except Exception as e:
        error_logger.error("An error occurred during execution", exc_info=True)
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
