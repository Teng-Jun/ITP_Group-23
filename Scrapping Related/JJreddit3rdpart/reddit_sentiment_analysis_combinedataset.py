import os
import pandas as pd

# Define the directory containing the CSV files
directory = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart\redditcommentdataset'

# List to store individual dataframes
dataframes = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)
        print(f"Loaded {filename}")

# Combine all dataframes into a single dataframe
combined_df = pd.concat(dataframes, ignore_index=True)

# Remove duplicates based on all columns
cleaned_df = combined_df.drop_duplicates()

# Save the cleaned dataframe to a new CSV file
cleaned_output_path = os.path.join(directory, 'dataset_combined_cleaned_reddit_comments.csv')
cleaned_df.to_csv(cleaned_output_path, index=False)

print(f"All files combined, duplicates removed, and saved to {cleaned_output_path}")
