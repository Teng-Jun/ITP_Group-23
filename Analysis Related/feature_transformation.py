import csv

# Load and process the dataset
input_file_path = 'airdrops_data_latest_ITP1_updated_with_temp.csv'
output_file_path = 'processed_airdrops_data_latest_ITP1_updated_with_temp.csv'

with open(input_file_path, mode='r', encoding='utf-8-sig') as infile, \
     open(output_file_path, mode='w', newline='', encoding='utf-8-sig') as outfile:
    
    reader = csv.DictReader(infile)
    # Define the new fieldnames to write in the output file
    fieldnames = ['Title', 'Num_Of_Prev_Drops', 'Whitepaper', 'Requirement_Count', 'Guide_Length', 'Social_Media_Count', 'Temp']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Handle the 'Whitepaper' field
        row['Whitepaper'] = 0 if row['Whitepaper'] == 'n/a' else 1
        
        # Convert 'Requirements' to count '|' plus one if not 'n/a', else 0
        row['Requirement_Count'] = row['Requirements'].count('|') + 1 if row['Requirements'] != 'n/a' else 0

        # Calculate the total number of steps in the 'Guide'
        # Assuming the guide is given as a list in the format '["step1.", "step2.", ..., "stepN."]'
        row['Guide_Length'] = len(eval(row['Guide']))

        # Count active social media links
        social_media_columns = [
            'Website', 'Facebook', 'Telegram Group', 'Telegram Channel', 'Discord', 
            'Twitter', 'Medium', 'CoinGecko', 'GitHub', 'Coinmarketcap', 
            'Reddit', 'Exchanges', 'Youtube'
        ]
        row['Social_Media_Count'] = sum(1 for field in social_media_columns if row[field] != 'n/a')

        # Retain the 'Temp' column without modifications
        row['Temp'] = row['Temp']  # This keeps the original temp value as it is

        # Write only the necessary fields
        writer.writerow({field: row[field] for field in fieldnames})

print("Data preprocessing is complete and written to", output_file_path)
