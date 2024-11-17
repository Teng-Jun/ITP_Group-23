import os
import pandas as pd
import torch
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
from datetime import datetime
from tqdm import tqdm
import csv
from sklearn.preprocessing import MinMaxScaler

# Set working directory and paths
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'

# Load datasets
reddit_data = pd.read_csv(os.path.join(DATA_PATH, 'combined_reddit_airdrop_data.csv'))
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of the first 1200 airdrop names
airdrop_names = airdrops_df['Title'].tolist()[:1200]  # Only first 1200

# Initialize the BERT sentiment analysis pipeline
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Initialize sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0, 'total_words': 0,
                               'total_upvotes': 0, 'comment_count': 0, 'average_comment_length': 0,
                               'scam_probability': 0.01, 'is_scam': False, 'total': 0} for airdrop in airdrop_names}

# Time Decay Formula: Decay Factor = 1 / (1 + lambda * days since post)
def time_decay(post_date, decay_lambda=0.01):
    post_datetime = datetime.utcfromtimestamp(post_date)  # Convert UTC to datetime
    days_since_post = (datetime.now() - post_datetime).days
    decay_factor = 1 / (1 + decay_lambda * days_since_post)
    return decay_factor

# Preprocess text
def preprocess_text(text):
    if pd.isna(text):
        return ''
    return text.lower()

# Perform sentiment analysis using BERT model
def perform_sentiment_analysis(text):
    try:
        # Truncate text to 512 tokens (BERT's max limit)
        text = text[:512]
        sentiment = sentiment_pipeline(text)
        if len(sentiment) > 0:
            label = sentiment[0]['label']
            score = sentiment[0]['score']
            
            # Map the BERT label to the sentiment category
            if label == "5 stars":  # Positive
                return score, 0, 0, len(text.split())
            elif label == "3 stars":  # Neutral
                return 0, score, 0, len(text.split())
            elif label in ["1 star", "2 stars"]:  # Negative
                return 0, 0, score, len(text.split())
        return 0, 0, 0, len(text.split())  # Neutral if no valid sentiment
    except Exception as e:
        print(f"Error processing text: {e}")
        return 0, 0, 0, len(text.split())  # Neutral if error occurs

# Temporary file path for saving progress
temp_file_path = "temporary_results_bert.csv"

# Perform sentiment analysis for each post and comment in the Reddit data
for index, row in tqdm(reddit_data.iterrows(), total=reddit_data.shape[0], desc="Analyzing sentiment"):
    title = preprocess_text(row.get('Title', ''))
    comment = preprocess_text(row.get('Comment', ''))
    post_date = row['Created_UTC']  # Use Created_UTC for time decay
    upvotes = row['Upvotes']  # Use Upvotes as the weight
    
    # Calculate time decay factor for the post
    decay_factor = time_decay(post_date)
    
    for airdrop in airdrop_names:
        # Check if the airdrop name is mentioned in the title or comment
        if airdrop.lower() in title or airdrop.lower() in comment:
            # Perform sentiment analysis on both title and comment
            title_pos, title_neu, title_neg, title_word_count = perform_sentiment_analysis(title)
            comment_pos, comment_neu, comment_neg, comment_word_count = perform_sentiment_analysis(comment)

            # Weighted sentiment calculation (taking time decay into account)
            weighted_title_pos = title_pos * decay_factor * upvotes
            weighted_title_neg = title_neg * decay_factor * upvotes
            weighted_comment_pos = comment_pos * decay_factor * upvotes
            weighted_comment_neg = comment_neg * decay_factor * upvotes
            
            # Aggregate sentiment counts for the airdrop
            sentiment_results[airdrop]['positive'] += weighted_title_pos + weighted_comment_pos
            sentiment_results[airdrop]['negative'] += weighted_title_neg + weighted_comment_neg
            sentiment_results[airdrop]['total_words'] += title_word_count + comment_word_count
            sentiment_results[airdrop]['total_upvotes'] += upvotes
            sentiment_results[airdrop]['comment_count'] += 1
            sentiment_results[airdrop]['average_comment_length'] += len(comment.split())

    # Periodically save progress to a temporary CSV file (e.g., every 1000 rows)
    if index % 1000 == 0:
        print(f"Saving progress at row {index}...")
        temp_df = pd.DataFrame.from_dict(sentiment_results, orient='index')
        temp_df.to_csv(temp_file_path)
        print(f"Temporary results saved to {temp_file_path}")

# Calculate final scam probability and whether it's a scam
for airdrop, sentiments in sentiment_results.items():
    total_sentiment = sentiments['positive'] + sentiments['neutral'] + sentiments['negative']
    total_words = sentiments['total_words']
    
    if total_sentiment > 0 and total_words > 0:
        sentiments['positive_percentage'] = (sentiments['positive'] / total_sentiment) * 100
        sentiments['neutral_percentage'] = (sentiments['neutral'] / total_sentiment) * 100
        sentiments['negative_percentage'] = (sentiments['negative'] / total_sentiment) * 100

        # Calculate scam probability: (negative - positive) / total_words
        scam_probability = (sentiments['negative'] - sentiments['positive']) / total_words
        sentiments['scam_probability'] = scam_probability
        sentiments['is_scam'] = scam_probability > 0.01
    else:
        sentiments['positive_percentage'] = 0
        sentiments['neutral_percentage'] = 0
        sentiments['negative_percentage'] = 0
        sentiments['scam_probability'] = 0
        sentiments['is_scam'] = False

# Save the final sentiment analysis results to a CSV file
final_output_file = 'bert_time_decay_weighted_sentiment_results.csv'
sentiment_results_df = pd.DataFrame.from_dict(sentiment_results, orient='index')
sentiment_results_df.to_csv(final_output_file)

print(f"Sentiment analysis results saved to {final_output_file}")
