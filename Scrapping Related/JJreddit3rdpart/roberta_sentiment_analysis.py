import os
import pandas as pd
import torch
from transformers import pipeline, RobertaTokenizer, RobertaForSequenceClassification
from tqdm import tqdm
import csv

# Set working directory and paths
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'

# Load datasets
reddit_data = pd.read_csv(os.path.join(DATA_PATH, 'combined_reddit_airdrop_data.csv'))
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of the first 800 airdrop names
#airdrop_names = airdrops_df['Title'].tolist()[:800]  # Only first 800

#airdrop_names = airdrops_df['Title'].tolist()[800:1600]  # Next 800

airdrop_names = airdrops_df['Title'].tolist()[1600:]  # Remaining airdrops

# Initialize the RoBERTa sentiment analysis pipeline
model_name = "cardiffnlp/twitter-roberta-base-sentiment"
model = RobertaForSequenceClassification.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Initialize sentiment results for each airdrop
sentiment_results = {airdrop: {'positive': 0, 'neutral': 0, 'negative': 0, 'total_words': 0} for airdrop in airdrop_names}

def preprocess_text(text):
    """Preprocess text by converting to lowercase and removing punctuation."""
    if pd.isna(text):
        return ''
    return text.lower()

def perform_roberta_sentiment_analysis(text):
    """Analyze sentiment using RoBERTa and classify into positive, neutral, and negative."""
    # Tokenize the input and truncate to the maximum length of 512 tokens
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the label and score
    scores = outputs.logits.softmax(dim=-1).cpu().numpy()
    label_id = scores.argmax(axis=1)[0]
    score = scores[0][label_id]

    # Map the RoBERTa label to the sentiment category
    if label_id == 2:  # Positive
        return score, 0, 0, len(text.split())
    elif label_id == 1:  # Neutral
        return 0, score, 0, len(text.split())
    elif label_id == 0:  # Negative
        return 0, 0, score, len(text.split())

# Perform sentiment analysis for each post and comment in the Reddit data
for index, row in tqdm(reddit_data.iterrows(), total=reddit_data.shape[0], desc="Analyzing sentiment"):
    title = preprocess_text(row.get('Title', ''))
    comment = preprocess_text(row.get('Comment', ''))

    for airdrop in airdrop_names:
        # Check if the airdrop name is mentioned in the title or comment
        if airdrop.lower() in title or airdrop.lower() in comment:
            # Analyze sentiment using RoBERTa
            title_pos, title_neu, title_neg, title_word_count = perform_roberta_sentiment_analysis(title)
            comment_pos, comment_neu, comment_neg, comment_word_count = perform_roberta_sentiment_analysis(comment)

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
output_file = 'roberta_airdrop_sentiment_results_part3.csv'  # Save as part 3
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

print(f"Sentiment analysis results with RoBERTa (Part 3) saved to {output_file}")
