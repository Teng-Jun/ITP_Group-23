import pandas as pd
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import os

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Set working directory
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'

# Load the datasets
reddit_data = pd.read_csv(os.path.join(DATA_PATH, 'combined_reddit_airdrop_data.csv'))
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of all airdrop names from the airdrop dataset
airdrop_names = airdrops_df['Title'].tolist()

# Initialize sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0, 'total_words': 0} for airdrop in airdrop_names}

def preprocess_text(text):
    """Preprocess text by converting to lowercase and removing punctuation."""
    if pd.isna(text):
        return ''
    return text.lower()

def perform_vader_sentiment_analysis(text):
    """Analyze sentiment using VADER."""
    sentiment = analyzer.polarity_scores(text)
    return sentiment['pos'], sentiment['neu'], sentiment['neg'], len(text.split())  # Return word count too

# Perform sentiment analysis for each post and comment in the Reddit data
for index, row in tqdm(reddit_data.iterrows(), total=reddit_data.shape[0], desc="Analyzing sentiment"):
    title = preprocess_text(row.get('Title', ''))
    comment = preprocess_text(row.get('Comment', ''))

    for airdrop in airdrop_names:
        # Check if the airdrop name is mentioned in the title or comment
        if airdrop.lower() in title or airdrop.lower() in comment:
            # Analyze sentiment using VADER
            title_pos, title_neu, title_neg, title_word_count = perform_vader_sentiment_analysis(title)
            comment_pos, comment_neu, comment_neg, comment_word_count = perform_vader_sentiment_analysis(comment)

            # Aggregate sentiment counts for the airdrop
            sentiment_results[airdrop]['positive'] += title_pos + comment_pos
            sentiment_results[airdrop]['neutral'] += title_neu + comment_neu
            sentiment_results[airdrop]['negative'] += title_neg + comment_neg
            sentiment_results[airdrop]['total_words'] += title_word_count + comment_word_count

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
        sentiments['is_scam'] = scam_probability > 0.3
    else:
        sentiments['positive_percentage'] = 0
        sentiments['neutral_percentage'] = 0
        sentiments['negative_percentage'] = 0
        sentiments['scam_probability'] = 0
        sentiments['is_scam'] = False

# Save the sentiment analysis results to a CSV file
output_file = 'vader_airdrop_sentiment_results_1.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'airdrop_name', 'positive', 'neutral', 'negative', 'total', 'total_words',
        'positive_percentage', 'neutral_percentage', 'negative_percentage',
        'scam_probability', 'is_scam'
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
            'is_scam': sentiments['is_scam']
        })

print(f"Sentiment analysis results with word count saved to {output_file}")
