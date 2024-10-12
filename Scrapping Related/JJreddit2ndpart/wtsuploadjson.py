import pandas as pd
import json
import logging
import os
import paramiko

# Change to the correct working directory
os.chdir(r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit2ndpart')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logging.basicConfig(filename='task_scheduler_error.log', level=logging.DEBUG)

# SSH and SCP Configuration
SSH_HOST = "13.76.25.253"
SSH_USER = "itpgroup23"
SSH_PASSWORD = "xji],x4~hSTBCqd"
REMOTE_DIR = "/var/www/html/AirGuard/data/"
JSON_SAVE_DIR = 'C:/Users/dclit/OneDrive/Documents/GitHub/ITP_Group-23/Website Related/AirGuard/data/'

# Function to combine and update CSV files correctly without adding extra columns
def combine_csv_files():
    try:
        logger.info("Loading CSV files...")
        new_data = pd.read_csv('new_airdrop_sentiment_results_version3.csv')
        old_data = pd.read_csv('combined_airdrop_sentiment_results_2.csv')

        # Ensure both DataFrames contain the same columns
        columns = [
            'airdrop_name', 'positive', 'neutral', 'negative', 
            'total', 'positive_percentage', 'neutral_percentage', 'negative_percentage'
        ]
        new_data = new_data[columns]
        old_data = old_data[columns]

        logger.info("Merging and updating counts...")

        # Merge the two datasets on 'airdrop_name'
        merged_data = pd.merge(
            old_data, new_data, on='airdrop_name', how='outer', suffixes=('_old', '_new')
        )

        # Update the values only if the new data has higher counts
        for column in ['positive', 'neutral', 'negative', 'total']:
            merged_data[column] = merged_data[[f"{column}_old", f"{column}_new"]].max(axis=1)

        # Update the percentages based on the latest 'total' value
        merged_data['positive_percentage'] = (merged_data['positive'] / merged_data['total']) * 100
        merged_data['neutral_percentage'] = (merged_data['neutral'] / merged_data['total']) * 100
        merged_data['negative_percentage'] = (merged_data['negative'] / merged_data['total']) * 100

        # Drop the temporary columns used for merging
        merged_data = merged_data[columns]

        # Save the final combined CSV
        combined_csv_file = 'combined_airdrop_sentiment_results_final.csv'
        merged_data.to_csv(combined_csv_file, index=False)
        logger.info(f"Combined CSV saved to {combined_csv_file}")

        return merged_data

    except Exception as e:
        logger.error(f"Failed to combine CSV files: {e}")
        raise

# Function to convert CSV to JSON
def save_to_json(combined_data):
    try:
        json_file = os.path.join(JSON_SAVE_DIR, 'sentiment_results_updated.json')
        combined_data.to_json(json_file, orient='records')
        logger.info(f"JSON saved to {json_file}")
        return json_file

    except Exception as e:
        logger.error(f"Failed to save to JSON: {e}")
        raise

# Function to upload JSON file to server
def upload_to_server(json_file):
    try:
        logger.info("Establishing SSH connection...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_HOST, username=SSH_USER, password=SSH_PASSWORD)

        sftp = ssh.open_sftp()
        remote_file_path = os.path.join(REMOTE_DIR, os.path.basename(json_file))

        logger.info(f"Uploading {json_file} to {remote_file_path}")
        sftp.put(json_file, remote_file_path)

        sftp.close()
        ssh.close()
        logger.info("Upload completed successfully.")

    except Exception as e:
        logger.error(f"Failed to upload to server: {e}")
        raise

# Main function to orchestrate the process
def main():
    try:
        logger.info("Starting the CSV combination process...")
        combined_data = combine_csv_files()

        logger.info("Converting combined CSV to JSON...")
        json_file = save_to_json(combined_data)

        logger.info("Uploading JSON to server...")
        upload_to_server(json_file)

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
