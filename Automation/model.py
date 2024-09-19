import csv
import mysql.connector
from db_config import DB_CONFIG

# Upload data to MySQL database
def upload_to_mysql(input_file):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL query to insert data into the `airdrops_data` table
        sql = """
        INSERT INTO airdrops_data (
            Title, Features, Guide, Total_Value, Status, Platform, Requirements,
            Num_Of_Prev_Drops, Website, Ticker, Total_Supply, Whitepaper, Thumbnail,
            Facebook, `Telegram Group`, `Telegram Channel`, Discord, Twitter, Medium,
            CoinGecko, GitHub, Coinmarketcap, Reddit, Exchanges, Youtube, Probability
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Open the CSV file and insert each row into the database
        with open(input_file, mode='r', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                try:
                    cursor.execute(sql, (
                        row['Title'], row['Features'], row['Guide'], row['Total_Value'], row['Status'],
                        row['Platform'], row['Requirements'], int(row['Num_Of_Prev_Drops']), row['Website'], row['Ticker'],
                        row['Total_Supply'], row['Whitepaper'], row['Thumbnail'], row['Facebook'], row['Telegram Group'],
                        row['Telegram Channel'], row['Discord'], row['Twitter'], row['Medium'], row['CoinGecko'],
                        row['GitHub'], row['Coinmarketcap'], row['Reddit'], row['Exchanges'], row['Youtube'],
                        int(row['Probability'])  # Ensure Probability is an integer
                    ))
                except KeyError as e:
                    print(f"Missing key in row: {e}")
                except Exception as e:
                    print(f"Error inserting row into database: {e}")

        connection.commit()
        print("Data uploaded to MySQL successfully.")

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
    
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
        print("MySQL connection closed.")

# Add Probability column to the CSV file
def add_probability_to_csv():
    input_file = 'airdrops_data_latest.csv'
    probability_file = 'real_data_with_predictions_RF.csv'
    output_file = 'airdrops_data_latest_updated.csv'

    # Read probabilities into a dictionary from real_data_with_predictions_RF.csv
    title_to_probability = {}
    with open(probability_file, mode='r', encoding='utf-8-sig') as prob_file:
        reader = csv.DictReader(prob_file)
        for row in reader:
            title_to_probability[row['Title']] = row['Probability']

    # Read the input CSV file and add the Probability column
    with open(input_file, mode='r', encoding='utf-8-sig') as infile, open(output_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['Probability']  # Add the Probability column
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write rows with the new Probability column
        for row in reader:
            title = row['Title']
            # Set Probability; use 0 if not found in the probability file
            row['Probability'] = title_to_probability.get(title, '0')
            writer.writerow(row)

    print(f"Probability column added to '{output_file}'.")

# Main processing function
def main():
    try:
        # Add Probability to the airdrops_data_latest.csv
        add_probability_to_csv()

        # Upload to MySQL using the updated CSV file
        upload_to_mysql('airdrops_data_latest_updated.csv')

    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
