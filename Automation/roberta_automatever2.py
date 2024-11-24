import os
import pandas as pd
import json
import praw
import prawcore
import logging
from tqdm import tqdm
import random
import re
import paramiko
from datetime import datetime, timezone, time
from transformers import pipeline, RobertaTokenizer, RobertaForSequenceClassification


# SSH Configuration
SSH_HOST = "13.76.25.253"
SSH_USER = "itpgroup23"
SSH_PASSWORD = "xji],x4~hSTBCqd"
REMOTE_DIR = "/var/www/html/AirGuard/data/"  # Destination directory on the server
JSON_LOCAL_DIR = 'C:/Users/dclit/OneDrive/Documents/GitHub/ITP_Group-23/Automation'

# Initialize RoBERTa sentiment analysis pipeline
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('script_log.log', 'w', 'utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Reddit API credentials
reddit = praw.Reddit(
    client_id='LmoF1XOmk2ejtYc-4mcevg',
    client_secret='LBebw5DAtL4K7-UaaZlKab2za9Uq3Q',
    user_agent='script:airdrop_scam_detector:v1.0 (by u/JJSIM98)'
)

def load_csv_with_encoding(filepath):
    """Load CSV with multiple encoding attempts."""
    encodings = ['utf-8', 'latin1', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to read {filepath}")

def preprocess_text(text):
    """Preprocess text for analysis."""
    if pd.isna(text):
        return ''
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text

def time_decay(post_date, decay_lambda=0.01):
    """Calculate time decay factor."""
    post_datetime = datetime.fromtimestamp(post_date, tz=timezone.utc)  # Use timezone.utc
    days_since_post = (datetime.now(tz=timezone.utc) - post_datetime).days
    decay_factor = 1 / (1 + decay_lambda * days_since_post)
    return decay_factor

def scrape_new_airdrop_data():
    """Get new airdrops to analyze."""
    try:
        latest_airdrops = load_csv_with_encoding('airdrops_data_latest.csv')
        try:
            sentiment_results = load_csv_with_encoding('roberta_time_decay_weighted_sentiment_results.csv')
        except FileNotFoundError:
            sentiment_results = pd.DataFrame(columns=['airdrop_name'])
        # Ensure both columns are in lowercase and stripped of leading/trailing whitespaces for accurate comparison
        logger.debug(f"Latest airdrops: {latest_airdrops['Title'].tolist()}")
        logger.debug(f"Processed airdrops: {sentiment_results['airdrop_name'].tolist()}")
        #latest_airdrops['Title'] = latest_airdrops['Title'].str.strip().str.lower()
        #sentiment_results['airdrop_name'] = sentiment_results['airdrop_name'].str.strip().str.lower()
        no_count_airdrops = sentiment_results[sentiment_results['total_words'] == 0]['airdrop_name'].tolist()
        new_airdrops = latest_airdrops[~latest_airdrops['Title'].isin(sentiment_results['airdrop_name'])]['Title'].tolist()
        logger.debug(f"Latest airdrops: {latest_airdrops['Title'].tolist()}")
        logger.debug(f"Processed airdrops: {sentiment_results['airdrop_name'].tolist()}")
        logger.debug(f"New airdrops identified: {new_airdrops + no_count_airdrops}")
        airdrop_names_to_scrape = list(set(new_airdrops + no_count_airdrops))[:10]
        logger.info(f"Found airdrops to analyze: {airdrop_names_to_scrape}")
        return sorted(airdrop_names_to_scrape)
    except Exception as e:
        logger.error(f"Error in scrape_new_airdrop_data: {e}")
        return []

def search_reddit(query, limit):
    """Search Reddit with rate limiting."""
    while True:
        try:
            return list(reddit.subreddit('all').search(query, limit=limit))
        except prawcore.exceptions.TooManyRequests as e:
            wait_time = int(e.response.headers.get('retry-after', 60)) + random.randint(1, 30)
            logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds.")
            time.sleep(wait_time)

def process_comments(comment, submission):
    """Process Reddit comments recursively."""
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
        for reply in comment.replies[:10]:
            comments_data.extend(process_comments(reply, submission))
    return comments_data

def perform_roberta_sentiment_analysis(text):
    """Perform sentiment analysis using RoBERTa model."""
    try:
        if not text or len(text.strip()) == 0:
            logger.debug("Empty or invalid text encountered.")
            return 0, 0, 0

        text = text[:512]  # Truncate to RoBERTa's limit
        sentiment = sentiment_pipeline(text)
        logger.debug(f"Sentiment raw output: {sentiment}")

        if not sentiment:
            return 0, 0, 0

        label = sentiment[0]['label']
        score = sentiment[0]['score']
        word_count = len(text.split())

        # RoBERTa's labels are:
        # LABEL_0 = negative, LABEL_2 = positive
        if label == "LABEL_2":  # Positive
            return score, 0, word_count
        elif label == "LABEL_0":  # Negative
            return 0, score, word_count

        logger.debug("No valid sentiment detected; returning default.")
        return 0, 0, word_count
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return 0, 0, 0

def convert_csv_to_json(csv_path, json_path):
    """Convert a CSV file to JSON format."""
    try:
        # Load the CSV into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Convert the DataFrame to a list of dictionaries (JSON array format)
        json_data = df.to_dict(orient='records')
        
        # Write the JSON data to a file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        logger.info(f"CSV successfully converted to JSON: {json_path}")
    except Exception as e:
        logger.error(f"Error converting CSV to JSON: {e}")

def merge_and_update_results(new_sentiment_results):
    """Merges new sentiment results with existing ones and updates the master file."""
    try:
        if not new_sentiment_results:  # Check if the input dictionary is empty
            logger.warning("No new sentiment results to update.")
            return  # Exit the function early

        new_results_df = pd.DataFrame.from_dict(new_sentiment_results, orient='index').reset_index()
        new_results_df.rename(columns={'index': 'airdrop_name'}, inplace=True)

        # Ensure 'positive' and 'negative' columns exist and handle empty DataFrame
        if 'positive' not in new_results_df.columns or 'negative' not in new_results_df.columns:
            logger.error("Missing 'positive' or 'negative' columns in the results.")
            return

        new_results_df['total'] = new_results_df['positive'] + new_results_df['negative']
        for sentiment in ['positive', 'negative']:
            new_results_df[f'{sentiment}_percentage'] = new_results_df.apply(
                lambda row: (row[sentiment] / row['total'] * 100) if row['total'] > 0 else 0,
                axis=1
            )

        # Calculate scam probability and is_scam
        new_results_df['scam_probability'] = new_results_df.apply(
            lambda row: (row['negative'] - row['positive']) / row['total_words'] if row['total_words'] > 0 else 0,
            axis=1
        )
        new_results_df['is_scam'] = new_results_df['scam_probability'] > 0.01

        existing_results_path = 'roberta_time_decay_weighted_sentiment_results.csv'
        if os.path.exists(existing_results_path):
            existing_df = load_csv_with_encoding(existing_results_path)
        else:
            existing_df = pd.DataFrame(columns=[
                'airdrop_name', 'positive', 'neutral', 'negative', 'total_words',
                'total_upvotes', 'comment_count', 'average_comment_length',
                'scam_probability', 'is_scam', 'total',
                'positive_percentage', 'negative_percentage'
            ])

        for idx, row in new_results_df.iterrows():
            existing_df = existing_df[existing_df['airdrop_name'] != row['airdrop_name']]
            existing_df = pd.concat([existing_df, pd.DataFrame([row])], ignore_index=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing_df.to_csv(existing_results_path, index=False)
        backup_path = f'sentiment_results_backup_{timestamp}.csv'
        existing_df.to_csv(backup_path, index=False)
        logger.info(f"Results saved to {existing_results_path} and {backup_path}")

        # Convert CSV to JSON
        convert_csv_to_json(existing_results_path, 'roberta_sentiment_results.json')

        return existing_df
    except Exception as e:
        logger.error(f"Error in merge_and_update_results: {e}", exc_info=True)
        raise
def upload_json_to_server(local_json_filename):
    """Uploads a JSON file to the remote SSH server."""
    try:
        local_file_path = os.path.join(JSON_LOCAL_DIR, local_json_filename)
        if not os.path.exists(local_file_path):
            logger.error(f"Local file does not exist: {local_file_path}")
            return

        logger.info("Establishing SSH connection...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

        sftp = ssh.open_sftp()
        remote_file_path = os.path.join(REMOTE_DIR, local_json_filename)

        logger.info(f"Uploading {local_file_path} to {remote_file_path}...")
        sftp.put(local_file_path, remote_file_path)

        sftp.close()
        ssh.close()
        logger.info("JSON file uploaded successfully.")
    except Exception as e:
        logger.error(f"Failed to upload JSON to server: {e}")
        raise

def main():
    try:
        airdrop_names_to_scrape = scrape_new_airdrop_data()  # Ensure this is called before checking
        
        if not airdrop_names_to_scrape:  # If no new airdrops, update existing results
            logger.info("No new airdrops to process. Proceeding to update existing results.")
             # Assuming you have already saved the JSON file in the specified directory
            json_filename = "roberta_sentiment_results.json"  # Replace with your JSON filename
            logger.info("Starting JSON upload to server...")
            upload_json_to_server(json_filename)
            sentiment_results = {}
            try:
                merge_and_update_results(sentiment_results)
            except Exception as e:
                logger.error(f"Error updating results for existing airdrops: {e}")
            return

        logger.info("Starting Reddit comment scraping...")
        reddit_data = []
        for airdrop in airdrop_names_to_scrape:
            search_queries = [
                f'"{airdrop}" cryptocurrency',
                f'"{airdrop}" airdrop',
                f'{airdrop} crypto'
            ]
            for query in search_queries:
                submissions = search_reddit(query, 10)
                for submission in submissions:
                    submission.comments.replace_more(limit=1)
                    for comment in submission.comments.list()[:10]:
                        reddit_data.extend(process_comments(comment, submission))

        pd.DataFrame(reddit_data).to_csv('intermediate_reddit_data.csv', index=False)

        logger.info("Starting sentiment analysis...")
        sentiment_results = {airdrop: {
            'positive': 0, 'negative': 0, 'neutral': 0,
            'total_words': 0, 'total_upvotes': 0,
            'comment_count': 0, 'average_comment_length': 0,
            'scam_probability': 0.01, 'is_scam': False, 'total': 0, 'neutral_percentage': 0
        } for airdrop in airdrop_names_to_scrape}

        for data in tqdm(reddit_data, desc="Analyzing comments"):
            title = preprocess_text(data.get('Title', ''))  # Safeguard missing or invalid keys
            comment = preprocess_text(data.get('Comment', ''))
            post_date = data.get('Created_UTC', 0)  # Default to 0 if missing
            upvotes = data.get('Upvotes', 0)  # Default to 0 if missing

            # Skip processing if post_date or upvotes are invalid
            if not isinstance(post_date, (int, float)):
                logger.warning(f"Invalid post_date: {post_date}")
                continue
            if not isinstance(upvotes, (int, float)):
                logger.warning(f"Invalid upvotes: {upvotes}")
                continue

            decay_factor = time_decay(post_date)
            for airdrop in airdrop_names_to_scrape:
                if isinstance(title, str) and isinstance(comment, str):  # Ensure both are strings
                    if airdrop.lower() in title.lower() or airdrop.lower() in comment.lower():
                        title_pos, title_neg, title_words = perform_roberta_sentiment_analysis(title)
                        comment_pos, comment_neg, comment_words = perform_roberta_sentiment_analysis(comment)

                        weight = decay_factor * upvotes
                        sentiment_results[airdrop]['positive'] += (title_pos + comment_pos) * weight
                        sentiment_results[airdrop]['negative'] += (title_neg + comment_neg) * weight
                        sentiment_results[airdrop]['total_words'] += title_words + comment_words
                        sentiment_results[airdrop]['total_upvotes'] += upvotes
                        sentiment_results[airdrop]['comment_count'] += 1

        merge_and_update_results(sentiment_results)
         # Assuming you have already saved the JSON file in the specified directory
        json_filename = "roberta_sentiment_results.json"  # Replace with your JSON filename
        logger.info("Starting JSON upload to server...")
        upload_json_to_server(json_filename)
        logger.info("Processing completed successfully")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()