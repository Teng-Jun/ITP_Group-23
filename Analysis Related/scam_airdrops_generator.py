import csv
import random

def generate_scam_title(index):
    return f"Scam_{index}"

# Paths to your files
input_file_path = 'processed_airdrops_data.csv'
output_file_path = 'combined_dataset_with_scam.csv'

# Open and read the existing data to determine fieldnames
with open(input_file_path, mode='r', newline='', encoding='utf-8-sig') as infile:
    reader = csv.DictReader(infile)
    existing_fieldnames = reader.fieldnames  # Capture the fieldnames directly from the reader

    if 'is_scam' not in existing_fieldnames:
        existing_fieldnames.append('is_scam')  # Add 'is_scam' if not present

# Prepare to write both existing and new synthetic data to the output file
with open(output_file_path, mode='w', newline='', encoding='utf-8-sig') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=existing_fieldnames)
    writer.writeheader()

    # Re-open the input file to read and write existing data with 'is_scam' set to 0
    with open(input_file_path, mode='r', newline='', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            row['is_scam'] = 0
            writer.writerow(row)

    # Generate and write synthetic scam data starting with Scam_1 to Scam_1843
    num_scam_entries = 1843
    for i in range(1, num_scam_entries + 1):
        scam_title = generate_scam_title(i)
        scam_entry = {
            'Title': scam_title,
            'Num_Of_Prev_Drops': random.choices([0, 1], weights=[0.9, 0.1], k=1)[0],
            'Whitepaper': random.choices([0, 1], weights=[0.9, 0.1], k=1)[0],
            'Requirement_Count': random.choice([1,2]),
            'Guide_Length': random.choice([1, 2, 3, 4, 5, 6, 7]),
            'Social_Media_Count': random.choice([1, 2]),
            'is_scam': 1
        }


        writer.writerow(scam_entry)

print("Synthetic scam data generated and combined with existing data in:", output_file_path)
