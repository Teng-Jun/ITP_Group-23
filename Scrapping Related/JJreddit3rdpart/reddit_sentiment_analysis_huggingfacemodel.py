from transformers import pipeline
import pandas as pd
from tqdm import tqdm
import time
import re

# Load a more nuanced sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Function to perform sentiment analysis using the Hugging Face model
def analyze_sentiment_hf(text):
    try:
        result = sentiment_analyzer(text[:512])[0]  # Limiting to the first 512 characters for compatibility
        label = result['label']  # Get the sentiment label (e.g., "1 star", "2 stars", etc.)
        score = result['score']  # Get the confidence score

        # Print the sentiment and score for debugging
        print(f"Text: {text[:30]}... | Sentiment: {label} | Score: {score}")

        # Map label to 'positive', 'neutral', 'negative'
        if label in ['4 stars', '5 stars']:
            return 'positive'
        elif label == '3 stars':
            return 'neutral'
        else:
            return 'negative'
    except Exception as e:
        print(f"Error processing text: {e}")
        return 'neutral'

# Load the Reddit comments dataset and limit it to the first 100 rows
reddit_comments_data = pd.read_csv('dataset_combined_cleaned_reddit_comments.csv')
airdrop_names = pd.read_csv('new_airdrops_data_latest.csv')['Title'].str.lower().tolist()

# Initialize a dictionary to store sentiment counts
sentiment_results_hf = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0} for airdrop in airdrop_names}

# Perform sentiment analysis on each comment using the Hugging Face model with progress bar and time tracking
start_time = time.time()
for index, row in tqdm(reddit_comments_data.iterrows(), total=reddit_comments_data.shape[0], desc="HF Sentiment Analysis"):
    comment = row['Comment']
    
    # Check if comment is a valid string
    if isinstance(comment, str):
        for airdrop in airdrop_names:
            # Use regex for more flexible matching
            if re.search(r'\b' + re.escape(airdrop) + r'\b', comment.lower()):
                sentiment = analyze_sentiment_hf(comment)
                sentiment_results_hf[airdrop][sentiment] += 1

# Calculate total counts and percentages for each airdrop
for airdrop, sentiments in sentiment_results_hf.items():
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

# Convert the results into a DataFrame for easy comparison
hf_sentiment_results_df = pd.DataFrame.from_dict(sentiment_results_hf, orient='index').reset_index()
hf_sentiment_results_df.rename(columns={'index': 'airdrop_name'}, inplace=True)

# Save the results to a CSV file
hf_sentiment_results_df.to_csv('hf_airdrop_sentiment_results_multiclass_v1.csv', index=False)

# Calculate the elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Sentiment analysis completed in {elapsed_time:.2f} seconds.")
print("Hugging Face-based sentiment analysis results saved to 'hf_airdrop_sentiment_results_multiclass_v1.csv'")
