import pandas as pd
import json
import logging
import os
import paramiko

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

# Function to combine CSV files
def combine_csv_files():
    try:
        logger.info("Loading CSV files...")
        new_data = pd.read_csv('new_airdrop_sentiment_results_version3.csv')  # Adjust path as needed
        old_data = pd.read_csv('combined_airdrop_sentiment_results_2.csv')    # Adjust path as needed

        logger.info("Combining CSV files...")
        combined_data = pd.concat([old_data, new_data]).drop_duplicates(subset='airdrop_name', keep='last')

        combined_csv_file = 'combined_airdrop_sentiment_results_final.csv'
        combined_data.to_csv(combined_csv_file, index=False)
        logger.info(f"Combined CSV saved to {combined_csv_file}")

        return combined_data

    except Exception as e:
        logger.error(f"Failed to combine CSV files: {e}")
        raise

# Function to convert CSV to JSON
def save_to_json(combined_data):
    try:
        json_file = JSON_SAVE_DIR + 'sentiment_results_updated.json'
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
        
        # Ensure that the file is uploaded to the correct directory and with the correct name
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
