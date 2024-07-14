import pandas as pd
from collections import Counter
import re
import csv
from tqdm import tqdm

# Load the CSV file with crawled Reddit data
reddit_data = pd.read_csv('combined_reddit_airdrop_data_version2.csv')

# Define word lists for sentiment analysis
positive_words = [
    'good', 'profitable', 'best', 'exciting', 'rewarding', 'beneficial', 'excellent', 'superior',
    'outstanding', 'amazing', 'delightful', 'brilliant', 'successful', 'advantageous', 'productive',
    'fruitful', 'lucrative', 'effective', 'worthwhile', 'constructive', 'valuable', 'enjoyable',
    'satisfying', 'wonderful', 'favorable', 'promising', 'enhancing', 'great', 'impressive',
    'perfect', 'positive', 'thriving', 'booming', 'winning', 'leading', 'innovative', 'pioneering',
    'revolutionary', 'game-changing', 'optimistic', 'glowing', 'acclaimed', 'recommended', 'epic',
    'majestic', 'splendid', 'miraculous', 'superb', 'magnificent'
]
neutral_words = [
    'stable', 'expected', 'normal', 'average', 'standard', 'common', 'regular', 'typical', 'ordinary',
    'usual', 'customary', 'conventional', 'median', 'moderate', 'neutral', 'unchanged', 'constant',
    'steady', 'routine', 'generic', 'uniform', 'balanced', 'fair', 'middle', 'adequate', 'plain',
    'simple', 'basic', 'unremarkable', 'undistinguished', 'standardized', 'normalized', 'unbiased',
    'straightforward', 'practical', 'functional', 'unexceptional', 'undramatic', 'unadorned',
    'unembellished'
]
negative_words = [
    'bad', 'loss', 'scam', 'risky', 'problematic', 'dangerous', 'poor', 'terrible', 'horrible',
    'dreadful', 'awful', 'troublesome', 'harmful', 'detrimental', 'disastrous', 'perilous',
    'hazardous', 'fatal', 'lethal', 'deadly', 'destructive', 'unfavorable', 'unpleasant', 'unhappy',
    'sad', 'depressing', 'gloomy', 'miserable', 'disappointing', 'insufficient', 'ineffective',
    'faulty', 'flawed', 'deficient', 'inferior', 'substandard', 'damaging', 'corrosive', 'cancerous',
    'toxic', 'vile', 'sinister', 'ominous', 'dire'
]

# Function to preprocess text
def preprocess_text(text):
    if pd.isna(text):
        return ''
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation and special characters
    return text

# Function to analyze sentiment
def analyze_sentiment(text, positive_words, neutral_words, negative_words):
    words = preprocess_text(text).split()
    word_counts = Counter(words)
    positive_count = sum(word_counts[word] for word in positive_words if word in word_counts)
    neutral_count = sum(word_counts[word] for word in neutral_words if word in word_counts)
    negative_count = sum(word_counts[word] for word in negative_words if word in word_counts)
    return positive_count, neutral_count, negative_count

# Load the CSV file with airdrop names
airdrops_df = pd.read_csv('airdrops_data_latest.csv')
airdrop_names = airdrops_df['Title'].tolist()

# Initialize a dictionary to store sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0} for airdrop in airdrop_names}

# Analyze sentiment for each post and comment in the Reddit data
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

# Write the sentiment results to a CSV file
output_file = 'new_airdrop_sentiment_results_version3.csv'
with open(output_file, 'w', newline='') as csvfile:
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

print(f"Sentiment analysis results saved to {output_file}")
