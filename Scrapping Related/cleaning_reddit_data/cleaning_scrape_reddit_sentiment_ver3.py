import pandas as pd
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

# Download NLTK data
nltk.download('vader_lexicon')
nltk.download('stopwords')

# Load the data
df = pd.read_csv('reddit_scam_data_ver3.csv')

# Remove rows with negative Comment_Upvotes
df_cleaned = df[df['Comment_Upvotes'] >= 0]

# Remove duplicate rows
df_cleaned = df_cleaned.drop_duplicates()

# Remove rows with missing values in critical columns
df_cleaned = df_cleaned.dropna(subset=['Comment', 'Title', 'Author', 'Comment_Author'])

# Standardize date formats
df_cleaned['Created_UTC'] = pd.to_datetime(df_cleaned['Created_UTC'], unit='s')

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
df_cleaned['Cleaned_Comment'] = df_cleaned['Comment'].apply(clean_text).apply(remove_stopwords)
df_cleaned['Cleaned_Title'] = df_cleaned['Title'].apply(clean_text).apply(remove_stopwords)

# Initialize VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Sentiment Analysis on Cleaned_Comment
df_cleaned['Sentiment_Score'] = df_cleaned['Cleaned_Comment'].apply(lambda x: sid.polarity_scores(x)['compound'])

# Flag and remove bot comments
bot_keywords = ['bot', 'automoderator', 'donut-bot']
df_cleaned = df_cleaned[~df_cleaned['Comment_Author'].str.contains('|'.join(bot_keywords), case=False)]

# Extract unique coins mentioned in the comments and titles
def extract_coins(text):
    # Extract words starting with '$' or coin symbols (optional implementation)
    coins = re.findall(r'\$\w+', text) + re.findall(r'\b\w+\b', text)
    return ' '.join(coins)

df_cleaned['Extracted_Coins_Comment'] = df_cleaned['Cleaned_Comment'].apply(extract_coins)
df_cleaned['Extracted_Coins_Title'] = df_cleaned['Cleaned_Title'].apply(extract_coins)

# Combine extracted coins from comments and titles
df_cleaned['Extracted_Coins'] = df_cleaned['Extracted_Coins_Comment'] + ' ' + df_cleaned['Extracted_Coins_Title']

# Remove stopwords again from the extracted coins
df_cleaned['Extracted_Coins'] = df_cleaned['Extracted_Coins'].apply(remove_stopwords)

# Aggregate unique coins mentioned
unique_coins = df_cleaned['Extracted_Coins'].str.split().explode().unique()

# Save cleaned data to a new CSV file
cleaned_csv_filename = 'cleaned_reddit_scam_data_ver4.csv'
df_cleaned.to_csv(cleaned_csv_filename, index=False)

# Save unique coins to a new CSV file
unique_coins_csv_filename = 'unique_coins_reddit_ver4.csv'
pd.DataFrame(unique_coins, columns=['Coin']).to_csv(unique_coins_csv_filename, index=False)

print(f"Cleaned data saved to {cleaned_csv_filename}")
print(f"Unique coins saved to {unique_coins_csv_filename}")
