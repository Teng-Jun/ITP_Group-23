import csv

# File paths
old_file_path = 'airdrops_data_latest_ITP1.csv'
new_file_path = 'airdrops_data_latest_ITP2.csv'
output_file_path = 'airdrops_data_latest_ITP1_updated_with_temp.csv'  # This will contain the updated data

# Load the new data (with Temp column)
new_data_dict = {}

with open(new_file_path, mode='r', encoding='utf-8-sig') as new_file:
    new_reader = csv.DictReader(new_file)
    
    for row in new_reader:
        # Use 'Title' as the key to match entries between the two files
        new_data_dict[row['Title']] = row['Temp']

# Load the old data (without Temp column) and update it with Temp from the new data
updated_rows = []

with open(old_file_path, mode='r', encoding='utf-8-sig') as old_file:
    old_reader = csv.DictReader(old_file)
    fieldnames = old_reader.fieldnames + ['Temp']  # Add the 'Temp' column to old fieldnames
    
    for row in old_reader:
        title = row['Title']
        
        # If the title exists in the new data, update the Temp column
        if title in new_data_dict:
            row['Temp'] = new_data_dict[title]
        else:
            row['Temp'] = '0°'  # Assign 'n/a' if Temp data is not available for this airdrop
        
        updated_rows.append(row)

# Write the updated data back to a new file
with open(output_file_path, mode='w', newline='', encoding='utf-8-sig') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Updated data saved to '{output_file_path}'")
