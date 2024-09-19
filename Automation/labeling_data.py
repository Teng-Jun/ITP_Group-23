import csv
import re

# File paths
input_file_path = 'processed_airdrops_data.csv'
output_file_path = 'processed_airdrops_data_labelled.csv'

# Define a function to sanitize the title
def sanitize_title(title):
    # Remove special characters, except alphanumeric and space
    return re.sub(r'[^a-zA-Z0-9 ]+', '', title)

def label_data():
    # Read the original data and write the modified data with the new column
    with open(input_file_path, mode='r', newline='', encoding='utf-8-sig') as infile, open(output_file_path, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read the header from the original file and append the new column name
        headers = next(reader)
        title_index = headers.index('Title')
        headers.append('is_scam')
        writer.writerow(headers)
        
        # Write the rest of the data, labeling all rows as 'not a scam'
        for row in reader:
            # Sanitize the title column
            row[title_index] = sanitize_title(row[title_index])
            # Label the row as 'not a scam'
            row.append('0')  # Append '0' indicating 'not a scam'
            writer.writerow(row)

    print("Data processed and written to", output_file_path)

def main():
    label_data()

if __name__ == "__main__":
    main()
