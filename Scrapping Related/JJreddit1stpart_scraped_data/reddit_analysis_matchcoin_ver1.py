import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from tqdm import tqdm

# Download NLTK data
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Load the Reddit data
df_reddit = pd.read_csv('cleaned_reddit_scam_data_ver4.csv')

# Load the CoinGecko data
df_coingecko = pd.read_csv('coingecko_coins_list_ver1.csv')

# Remove rows with negative Comment_Upvotes in Reddit data
df_reddit_cleaned = df_reddit[df_reddit['Comment_Upvotes'] >= 0]

# Remove duplicate rows in Reddit data
df_reddit_cleaned = df_reddit_cleaned.drop_duplicates()

# Remove rows with missing values in critical columns in Reddit data
df_reddit_cleaned = df_reddit_cleaned.dropna(subset=['Comment', 'Title', 'Author', 'Comment_Author'])

# Data Cleaning Function
def clean_text(text):
    text = str(text).lower()  # Convert to lowercase and ensure it's a string
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

# Remove stopwords
stop_words = set(stopwords.words('english'))
def remove_stopwords(text):
    words = text.split()
    return ' '.join([word for word in words if word not in stop_words])

# Clean and remove stopwords from text columns
df_reddit_cleaned['Cleaned_Comment'] = df_reddit_cleaned['Comment'].apply(lambda x: clean_text(x) if pd.notnull(x) else "")
df_reddit_cleaned['Cleaned_Title'] = df_reddit_cleaned['Title'].apply(clean_text).apply(remove_stopwords)

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Sentiment Analysis on Cleaned_Comment
df_reddit_cleaned['Sentiment_Score'] = df_reddit_cleaned['Cleaned_Comment'].apply(lambda x: sid.polarity_scores(x)['compound'] if isinstance(x, str) else 0)

# Flag and remove bot comments in Reddit data
bot_keywords = ['bot', 'automoderator', 'donut-bot']
df_reddit_cleaned = df_reddit_cleaned[~df_reddit_cleaned['Comment_Author'].str.contains('|'.join(bot_keywords), case=False)]

# Extract unique coins mentioned in the titles
def extract_coins(text):
    # Extract words starting with '$' or coin symbols (optional implementation)
    coins = re.findall(r'\$\w+', text) + re.findall(r'\b\w+\b', text)
    return ' '.join(coins)

df_reddit_cleaned['Extracted_Coins_Title'] = df_reddit_cleaned['Cleaned_Title'].apply(extract_coins)

# Remove stopwords again from the extracted coins
df_reddit_cleaned['Extracted_Coins_Title'] = df_reddit_cleaned['Extracted_Coins_Title'].apply(remove_stopwords)

# Aggregate unique coins mentioned
unique_coins = df_reddit_cleaned['Extracted_Coins_Title'].str.split().explode().unique()

# Create a lookup dictionary to keep track of matched coins
coin_lookup = {}

# Function to normalize coin names and symbols
def normalize_name(name):
    if isinstance(name, str):
        return ''.join(e for e in name.lower() if e.isalnum())
    return ''

# Normalize the coin symbols and names in CoinGecko data
df_coingecko['Cleaned_Symbol'] = df_coingecko['symbol'].apply(normalize_name)
df_coingecko['Cleaned_Name'] = df_coingecko['name'].apply(normalize_name)

# Compare extracted coins from Reddit data with CoinGecko data
matched_coins = []
for coin in tqdm(unique_coins, desc="Matching coins"):
    normalized_coin = normalize_name(coin)
    if normalized_coin in coin_lookup:
        matched_coins.append(coin_lookup[normalized_coin])
    else:
        match = df_coingecko[(df_coingecko['Cleaned_Symbol'] == normalized_coin) | (df_coingecko['Cleaned_Name'] == normalized_coin)]
        if not match.empty:
            coin_info = match.iloc[0].to_dict()
            coin_lookup[normalized_coin] = coin_info
            matched_coins.append(coin_info)

# Create a DataFrame to store matched coins with Reddit discussion URLs
matched_coins_with_urls = []
seen_titles = set()
for idx, row in df_reddit_cleaned.iterrows():
    if row['Title'] not in seen_titles:
        seen_titles.add(row['Title'])
        extracted_coins = row['Extracted_Coins_Title'].split()
        for coin in extracted_coins:
            normalized_coin = normalize_name(coin)
            if normalized_coin in coin_lookup:
                coin_info = coin_lookup[normalized_coin].copy()
                coin_info['reddit_url'] = row['URL']
                matched_coins_with_urls.append(coin_info)

# Save cleaned Reddit data and matched coins to CSV files
cleaned_csv_filename = 'cleaned_reddit_scam_data_ver4.csv'
df_reddit_cleaned.to_csv(cleaned_csv_filename, index=False)

matched_coins_csv_filename = 'matched_coins_reddit_ver4.csv'
pd.DataFrame(matched_coins_with_urls).to_csv(matched_coins_csv_filename, index=False)

print(f"Cleaned data saved to {cleaned_csv_filename}")
print(f"Matched coins saved to {matched_coins_csv_filename}")
