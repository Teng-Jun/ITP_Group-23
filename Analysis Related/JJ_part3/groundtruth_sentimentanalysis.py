import pandas as pd
import os

# Set working directory
DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Analysis Related\JJ_part3'

# Load the airdrop titles
airdrops_df = pd.read_csv(os.path.join(DATA_PATH, 'new_airdrops_data_latest.csv'))

# Get a list of all airdrop names
airdrop_names = airdrops_df['Title'].tolist()

# Load the scam tokens data
scam_data = pd.read_csv(os.path.join(DATA_PATH, 'scam_airdrop_data.csv'))

# Get a list of scam token names
scam_tokens = scam_data['Project Name'].tolist()  # Adjust column name if necessary

# Create ground truth labels
ground_truth = {
    "Token Name": [],
    "Is Scam": []
}

for airdrop in airdrop_names:
    ground_truth["Token Name"].append(airdrop)
    # Check if the airdrop name is in the scam tokens list
    if airdrop in scam_tokens:
        ground_truth["Is Scam"].append(1)  # Mark as scam
    else:
        ground_truth["Is Scam"].append(0)  # Mark as not scam

# Create a DataFrame for the ground truth
ground_truth_df = pd.DataFrame(ground_truth)

# Save the ground truth DataFrame to a CSV file
ground_truth_df.to_csv("ground_truth_labels.csv", index=False)

print("Ground truth labels created and saved as 'ground_truth_labels.csv'.")
