import pandas as pd
import os

# Define the directory and filenames
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'
csv_files = [
    os.path.join(DATA_PATH, 'bert_time_decay_weighted_sentiment_results_p1.csv'),
    os.path.join(DATA_PATH, 'bert_time_decay_weighted_sentiment_results_p2.csv'),
    #os.path.join(DATA_PATH, 'roberta_airdrop_sentiment_results_part3.csv')
]

# Combine all CSV files into one DataFrame
combined_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Save the combined CSV file
combined_df.to_csv(os.path.join(DATA_PATH, 'bert_time_decay_weighted_sentiment_results_combined.csv'), index=False)

print("All parts combined successfully!")
