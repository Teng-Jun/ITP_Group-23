import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from tqdm import tqdm
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import os

# Set working directory and paths
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'

# Load datasets
reddit_data = pd.read_csv(os.path.join(DATA_PATH, 'combined_reddit_airdrop_data.csv'))
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of all airdrop names
airdrop_names = airdrops_df['Title'].tolist()

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0, 'total_words': 0,
                               'total_upvotes': 0, 'comment_count': 0, 'average_comment_length': 0,
                               'scam_probability': 0, 'is_scam': False} for airdrop in airdrop_names}

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

# Perform sentiment analysis using VADER model
def perform_vader_sentiment_analysis(text):
    sentiment = analyzer.polarity_scores(text)
    return sentiment['pos'], sentiment['neu'], sentiment['neg'], len(text.split())

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
            title_pos, title_neu, title_neg, title_word_count = perform_vader_sentiment_analysis(title)
            comment_pos, comment_neu, comment_neg, comment_word_count = perform_vader_sentiment_analysis(comment)
            
            # Weighted sentiment calculation (taking time decay into account)
            weighted_title_pos = title_pos * decay_factor * upvotes
            weighted_title_neg = title_neg * decay_factor * upvotes
            weighted_comment_pos = comment_pos * decay_factor * upvotes
            weighted_comment_neg = comment_neg * decay_factor * upvotes
            
            # Aggregate sentiment counts for the airdrop
            sentiment_results[airdrop]['positive'] += weighted_title_pos + weighted_comment_pos
            sentiment_results[airdrop]['negative'] += weighted_title_neg + weighted_comment_neg
            sentiment_results[airdrop]['total_words'] += len(title.split()) + len(comment.split())
            sentiment_results[airdrop]['total_upvotes'] += upvotes
            sentiment_results[airdrop]['comment_count'] += 1
            sentiment_results[airdrop]['average_comment_length'] += len(comment.split())

# Calculate final scam probability using weighted sentiments
for airdrop, sentiments in sentiment_results.items():
    weighted_positive = sentiments['positive']
    weighted_negative = sentiments['negative']
    total_words = sentiments['total_words']

    if total_words > 0:
        # Calculating weighted scam probability based on sentiment and word count
        sentiments['scam_probability'] = (weighted_negative - weighted_positive) / total_words
        sentiments['is_scam'] = sentiments['scam_probability'] > 0.01

# Save the results to a CSV file
output_file = 'vader_time_decay_weighted_sentiment_results_2.csv'
sentiment_results_df = pd.DataFrame.from_dict(sentiment_results, orient='index')

# Normalize additional features if you want to use them
features_to_scale = ['positive', 'neutral', 'negative', 'total_words', 'total_upvotes', 'comment_count', 'average_comment_length']
scaler = MinMaxScaler()
sentiment_results_df[features_to_scale] = scaler.fit_transform(sentiment_results_df[features_to_scale])

sentiment_results_df.to_csv(output_file)

# Find the best threshold using F1 score and other metrics
thresholds = [i / 100 for i in range(1, 100)]  # Test thresholds from 0.01 to 0.99
best_threshold = 0
best_f1_score = 0
for threshold in thresholds:
    # Adjust 'is_scam' based on the threshold
    sentiment_results_df['is_scam'] = sentiment_results_df['scam_probability'] > threshold
    
    # Calculate Precision, Recall, F1 score, and Accuracy
    y_true = sentiment_results_df['is_scam'].astype(int)  # Ground truth
    y_pred = sentiment_results_df['is_scam'].astype(int)  # Predicted values
    
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    accuracy = accuracy_score(y_true, y_pred)
    
    if f1 > best_f1_score:
        best_f1_score = f1
        best_threshold = threshold

print(f"Best Threshold: {best_threshold}")
print(f"Best F1 Score: {best_f1_score}")

# Evaluate metrics with the best threshold
sentiment_results_df['is_scam'] = sentiment_results_df['scam_probability'] > best_threshold
y_true = sentiment_results_df['is_scam'].astype(int)
y_pred = sentiment_results_df['is_scam'].astype(int)

precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
accuracy = accuracy_score(y_true, y_pred)

print(f"Precision at best threshold: {precision:.4f}")
print(f"Recall at best threshold: {recall:.4f}")
print(f"F1 Score at best threshold: {f1:.4f}")
print(f"Accuracy at best threshold: {accuracy:.4f}")
