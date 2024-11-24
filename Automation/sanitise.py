import csv

# Define the path to your CSV file
file_path = 'airdrops_data_latest.csv'

def sanitize_data():
    # Temporary list to hold rows as they are processed
    updated_rows = []

    # Open the original CSV file for reading
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames

        # Process each row in the CSV
        for row in reader:
            # Convert 'Platform' to lowercase
            row['Platform'] = row['Platform'].lower()

            # Check and replace 'Exchanges' and 'Requirements' fields if they are empty
            for field in ['Status', 'Requirements', 'Ticker', 'Total_Supply', 'Facebook', 'Telegram Group', 'Telegram Channel', 'Medium', 'CoinGecko', 'GitHub', 'Coinmarketcap', 'Reddit', 'Exchanges', 'Youtube']:
                if not row[field].strip():
                    row[field] = 'n/a'

            # Clean up the 'Requirements' field
            if row['Requirements'] != 'n/a':
                parts = [part.strip() for part in row['Requirements'].split('|') if part.strip()]
                if not parts:
                    row['Requirements'] = 'n/a'
                else:
                    row['Requirements'] = ' | '.join(parts)
            
            if 'Temp' in row:
                row['Temp'] = row['Temp'].replace('°', '')

            updated_rows.append(row)

    # Open the file again, this time for writing
    with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()  # Write the headers to the CSV file
        writer.writerows(updated_rows)  # Write the updated rows back to the CSV file

    print("Updated data saved back to the original file.")

def main():
    sanitize_data()

if __name__ == "__main__":
    main()