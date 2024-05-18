import csv

# Define the path to your CSV file
file_path = 'airdrops_data_latest.csv'

# Temporary list to hold rows as they are processed
updated_rows = []

# Open the original CSV file for reading
with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    fields = reader.fieldnames
    
    # Process each row in the CSV
    for row in reader:
        # Check if the 'Exchanges' field is empty and replace it with 'n/a'
        if not row['Exchanges'].strip():
            row['Exchanges'] = 'n/a'
        
        # Similarly, check if the 'Requirements' field is empty and replace it with 'n/a'
        if not row['Requirements'].strip():
            row['Requirements'] = 'n/a'

        updated_rows.append(row)

# Open the file again, this time for writing
with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()  # Write the headers to the CSV file
    writer.writerows(updated_rows)  # Write the updated rows back to the CSV file

print("Updated data saved back to the original file.")




