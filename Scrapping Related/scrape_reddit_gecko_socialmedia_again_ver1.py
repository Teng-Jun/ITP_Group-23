import pandas as pd
import ast

# Load the matched coins data with URLs
matched_coins_df = pd.read_csv('matched_coins_with_details_reddit_ver4.csv')

# Function to process social media column
def process_social_media(social_media_str):
    social_media_dict = ast.literal_eval(social_media_str)
    twitter_url = f"https://twitter.com/{social_media_dict.get('Twitter')}" if social_media_dict.get('Twitter') else ''
    facebook_url = f"https://www.facebook.com/{social_media_dict.get('Facebook')}" if social_media_dict.get('Facebook') else ''
    reddit_url = social_media_dict.get('Reddit') if social_media_dict.get('Reddit') and social_media_dict.get('Reddit') != 'https://www.reddit.com' else ''
    return twitter_url, facebook_url, reddit_url

# Drop duplicate IDs
matched_coins_df.drop_duplicates(subset='id', inplace=True)

# Initialize new columns
matched_coins_df['Twitter'] = ''
matched_coins_df['Facebook'] = ''
matched_coins_df['Reddit'] = ''

# Process each row to separate social media links
for index, row in matched_coins_df.iterrows():
    twitter, facebook, reddit = process_social_media(row['Social_Media'])
    matched_coins_df.at[index, 'Twitter'] = twitter
    matched_coins_df.at[index, 'Facebook'] = facebook
    matched_coins_df.at[index, 'Reddit'] = reddit

# Drop the original Social_Media column
matched_coins_df.drop(columns=['Social_Media'], inplace=True)

# Save the updated DataFrame to a new CSV file
updated_csv_filename = 'matched_coins_with_details_reddit_ver7.csv'
matched_coins_df.to_csv(updated_csv_filename, index=False)

print(f"Updated matched coins data with details saved to {updated_csv_filename}")
