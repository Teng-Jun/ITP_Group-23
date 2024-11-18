import os
import pandas as pd
from collections import Counter
import re
import csv
from tqdm import tqdm
from datetime import datetime

# Custom word lists for sentiment analysis
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

# Set working directory
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'

# Load the datasets
reddit_data = pd.read_csv(os.path.join(DATA_PATH, 'combined_reddit_airdrop_data.csv'))
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of all airdrop names from the airdrop dataset
airdrop_names = airdrops_df['Title'].tolist()

# Initialize sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0, 'total_words': 0, 'total_upvotes': 0,
                               'comment_count': 0, 'average_comment_length': 0, 'scam_probability': 0.01, 'is_scam': False, 
                               'total': 0} for airdrop in airdrop_names}

# Time Decay Formula: Decay Factor = 1 / (1 + lambda * days since post)
def time_decay(post_date, decay_lambda=0.01):
    post_datetime = datetime.utcfromtimestamp(post_date)  # Convert UTC to datetime
    days_since_post = (datetime.now() - post_datetime).days
    decay_factor = 1 / (1 + decay_lambda * days_since_post)
    return decay_factor

# Function to preprocess text
def preprocess_text(text):
    if pd.isna(text):
        return ''
    return text.lower()

# Function to perform sentiment analysis using the custom dictionary
def analyze_custom_sentiment(text):
    words = preprocess_text(text).split()
    word_counts = Counter(words)
    positive_count = sum(word_counts[word] for word in positive_words if word in word_counts)
    neutral_count = sum(word_counts[word] for word in neutral_words if word in word_counts)
    negative_count = sum(word_counts[word] for word in negative_words if word in word_counts)
    total_words = len(words)
    return positive_count, neutral_count, negative_count, total_words

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
            # Analyze sentiment using custom dictionary
            title_pos, title_neu, title_neg, title_word_count = analyze_custom_sentiment(title)
            comment_pos, comment_neu, comment_neg, comment_word_count = analyze_custom_sentiment(comment)

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

# Calculate total counts, percentages, and scam probability
for airdrop, sentiments in sentiment_results.items():
    total_sentiment = sentiments['positive'] + sentiments['neutral'] + sentiments['negative']
    total_words = sentiments['total_words']
    sentiments['total'] = total_sentiment

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

# Save the sentiment analysis results to a CSV file
output_file = 'customdicwords_time_decay_weighted_sentiment_results.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'airdrop_name', 'positive', 'neutral', 'negative', 'total', 'total_words',
        'positive_percentage', 'neutral_percentage', 'negative_percentage',
        'scam_probability', 'is_scam', 'total_upvotes', 'comment_count', 'average_comment_length'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for airdrop, sentiments in sentiment_results.items():
        writer.writerow({
            'airdrop_name': airdrop,
            'positive': sentiments['positive'],
            'neutral': sentiments['neutral'],
            'negative': sentiments['negative'],
            'total': sentiments['total'],
            'total_words': sentiments['total_words'],
            'positive_percentage': sentiments['positive_percentage'],
            'neutral_percentage': sentiments['neutral_percentage'],
            'negative_percentage': sentiments['negative_percentage'],
            'scam_probability': sentiments['scam_probability'],
            'is_scam': sentiments['is_scam'],
            'total_upvotes': sentiments['total_upvotes'],
            'comment_count': sentiments['comment_count'],
            'average_comment_length': sentiments['average_comment_length']
        })

print(f"Sentiment analysis results with scam probability saved to {output_file}")