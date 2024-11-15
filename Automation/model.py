import pandas as pd
import mysql.connector
from db_config import DB_CONFIG
from sklearn.preprocessing import StandardScaler
import joblib
import csv

# Load model and scaler, make predictions, and save results with probability
def add_probability_to_csv():
    # Load the saved Random Forest model
    rf_model_filename = 'random_forest_model.joblib'
    rf_model = joblib.load(rf_model_filename)
    print("Random Forest model loaded successfully.")

    scaler_filename = 'scaler.joblib'
    scaler = joblib.load(scaler_filename)  # Load the previously saved scaler
    print("Scaler loaded successfully.")

    # Load the data to be predicted
    data_path = 'processed_airdrops_data_labelled.csv'
    real_data = pd.read_csv(data_path, encoding='ISO-8859-1')
    print("Real data loaded successfully.")

    # Assuming that real_data should be processed in the same way as your training data
    # Check if real_data contains the same features, exclude target feature if it exists
    if 'is_scam' in real_data.columns:
        X_real = real_data.drop(['Title', 'is_scam'], axis=1)
    else:
        X_real = real_data.drop(['Title'], axis=1)

    # Scale the features using the loaded scaler
    X_real_scaled = scaler.transform(X_real)

    # Make predictions with Random Forest
    rf_predictions = rf_model.predict(X_real_scaled)
    rf_probabilities = rf_model.predict_proba(X_real_scaled)[:, 1]

    # Add predictions to the data frame if needed
    real_data['Prediction'] = rf_predictions
    real_data['Probability'] = rf_probabilities.round(2)

    # Save or display the results
    output_path = 'real_data_with_predictions_RF.csv'
    real_data.to_csv(output_path, index=False)
    print(f"Predictions added and saved to {output_path}.")

# Append Probability to airdrops_data_latest.csv and save the updated CSV
def append_probability_to_airdrops():
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

# Upload data to MySQL database with update-on-duplicate functionality
def upload_to_mysql():
    input_file = 'airdrops_data_latest_updated.csv'
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # SQL query to insert data or update if it already exists (ON DUPLICATE KEY UPDATE)
        sql = """
        INSERT INTO airdrops_data (
            Title, Features, Guide, Total_Value, Status, Platform, Requirements,
            Num_Of_Prev_Drops, Website, Ticker, Total_Supply, Whitepaper, Thumbnail,
            Facebook, `Telegram Group`, `Telegram Channel`, Discord, Twitter, Medium,
            CoinGecko, GitHub, Coinmarketcap, Reddit, Exchanges, Youtube, Probability
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            Features=VALUES(Features),
            Guide=VALUES(Guide),
            Total_Value=VALUES(Total_Value),
            Status=VALUES(Status),
            Platform=VALUES(Platform),
            Requirements=VALUES(Requirements),
            Num_Of_Prev_Drops=VALUES(Num_Of_Prev_Drops),
            Website=VALUES(Website),
            Ticker=VALUES(Ticker),
            Total_Supply=VALUES(Total_Supply),
            Whitepaper=VALUES(Whitepaper),
            Thumbnail=VALUES(Thumbnail),
            Facebook=VALUES(Facebook),
            `Telegram Group`=VALUES(`Telegram Group`),
            `Telegram Channel`=VALUES(`Telegram Channel`),
            Discord=VALUES(Discord),
            Twitter=VALUES(Twitter),
            Medium=VALUES(Medium),
            CoinGecko=VALUES(CoinGecko),
            GitHub=VALUES(GitHub),
            Coinmarketcap=VALUES(Coinmarketcap),
            Reddit=VALUES(Reddit),
            Exchanges=VALUES(Exchanges),
            Youtube=VALUES(Youtube),
            Probability=VALUES(Probability)
        """

        # Open the CSV file and insert/update each row into the database
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
                        float(row['Probability'])  # Ensure Probability is a float
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

# Main processing function
def main():
    try:
        # Step 1: Add probability to real_data_with_predictions_RF.csv
        add_probability_to_csv()

        # Step 2: Append the probability column to airdrops_data_latest.csv
        append_probability_to_airdrops()

        # # Step 3: Upload the updated CSV to MySQL database
        upload_to_mysql()

    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()
