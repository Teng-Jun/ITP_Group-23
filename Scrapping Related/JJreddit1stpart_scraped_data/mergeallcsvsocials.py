import pandas as pd
import numpy as np

# Load all CSV files
df_ver8 = pd.read_csv('matched_coins_with_details_reddit_ver8.csv')
df_ver9 = pd.read_csv('matched_coins_with_details_reddit_ver9.csv')

# Ensure 'id' columns are strings to avoid any potential merge issues
df_ver8['id'] = df_ver8['id'].astype(str)
df_ver9['id'] = df_ver9['id'].astype(str)

# Ensure social media columns are strings to avoid any type issues
for df in [df_ver8, df_ver9]:
    df['Instagram'] = df['Instagram'].astype(str)
    df['Telegram'] = df['Telegram'].astype(str)
    df['Discord'] = df['Discord'].astype(str)

# Function to update master DataFrame with new data
def update_master(master_df, new_df, version_name):
    for index, row in new_df.iterrows():
        coin_id = row['id']
        if coin_id in master_df['id'].values:
            master_row_index = master_df.index[master_df['id'] == coin_id].tolist()[0]
            for column in ['Instagram', 'Telegram', 'Discord']:
                master_value = master_df.at[master_row_index, column]
                new_value = row[column]
                print(f"Processing {coin_id} - Index {index}")
                print(f"Checking {column}: master_df - {master_value}, new_df - {new_value}")
                if pd.isna(master_value) or master_value == '' or master_value == 'nan':
                    if new_value and new_value != 'nan' and new_value != 'nan':
                        print(f"Updating {column} for {coin_id} from {version_name}: {master_value} -> {new_value}")
                        master_df.at[master_row_index, column] = new_value
                else:
                    print(f"No update needed for {column} for {coin_id}")
        else:
            print(f"Coin ID {coin_id} not found in master_df")
            master_df = master_df.append(row, ignore_index=True)
    return master_df

# Initialize master DataFrame with ver8 data
master_df = df_ver8.copy()

# Update master DataFrame with ver9 data
master_df = update_master(master_df, df_ver9, "ver9")

# Ensure the combined DataFrame social media columns are strings
master_df['Instagram'] = master_df['Instagram'].astype(str)
master_df['Telegram'] = master_df['Telegram'].astype(str)
master_df['Discord'] = master_df['Discord'].astype(str)

# Save the combined DataFrame to a new CSV file
final_csv_path = 'combined_matched_coins_with_details.csv'
master_df.to_csv(final_csv_path, index=False)

print(f"Combined CSV saved at: {final_csv_path}")

# Display a few rows of the updated dataframe to check the content
print("Updated master_df:")
print(master_df[['id', 'Instagram', 'Telegram', 'Discord']].head(20))

# Reload the saved CSV to verify its content
reloaded_df = pd.read_csv(final_csv_path)
print("Reloaded CSV:")
print(reloaded_df[['id', 'Instagram', 'Telegram', 'Discord']].head(20))
