# import csv
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression

# # Load your dataset
# data = pd.read_csv('combined_dataset_with_scam.csv')

# # Prepare feature matrix X and target vector y
# X = data[['Num_Of_Prev_Drops', 'Whitepaper', 'Requirement_Count', 'Guide_Length', 'Social_Media_Count']]
# y = data['is_scam']

# # Split data into training and test sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# # Initialize and train the logistic regression model
# model = LogisticRegression()
# model.fit(X_train, y_train)

# # Predict probabilities on the full dataset for consistency
# full_probabilities = model.predict_proba(X)[:, 1]  # Get the probability of 'is_scam=1'

# # Read the existing CSV to append the new data
# with open('combined_dataset_with_scam.csv', mode='r', newline='', encoding='utf-8-sig') as infile, \
#      open('combined_dataset_with_scam_probabilities.csv', mode='w', newline='', encoding='utf-8-sig') as outfile:
    
#     reader = csv.DictReader(infile)
#     fieldnames = reader.fieldnames + ['Scam_Probability']  # add new field for scam probabilities
    
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()
    
#     # Iterate over the original data and the computed probabilities
#     for row, prob in zip(reader, full_probabilities):
#         row['Scam_Probability'] = f"{prob * 100:.2f}%"  # format probability as a percentage string
#         writer.writerow(row)

# print("Updated CSV with scam probabilities written to 'combined_dataset_with_scam_probabilities.csv'")


import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load your dataset
data = pd.read_csv('combined_dataset_with_scam.csv')

# Prepare feature matrix X and target vector y
X = data[['Num_Of_Prev_Drops', 'Whitepaper', 'Requirement_Count', 'Guide_Length', 'Social_Media_Count']]
y = data['is_scam']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict probabilities on the full dataset for consistency
full_probabilities = model.predict_proba(X)[:, 1]  # Get the probability of 'is_scam=1'

# Read the existing CSV to append the new data
with open('combined_dataset_with_scam.csv', mode='r', newline='', encoding='utf-8-sig') as infile, \
     open('combined_dataset_with_scam_probabilities.csv', mode='w', newline='', encoding='utf-8-sig') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['Scam_Probability']  # add new field for scam probabilities
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    # Iterate over the original data and the computed probabilities
    for row, prob in zip(reader, full_probabilities):
        # Convert probability to a percentage format, multiplying by 100
        formatted_probability = f"{prob * 100:.2f}%"  # format probability as a percentage string
        row['Scam_Probability'] = formatted_probability
        print(f"Debug: {prob} -> {formatted_probability}")  # Debug output to trace values
        writer.writerow(row)

print("Updated CSV with scam probabilities written to 'combined_dataset_with_scam_probabilities.csv'")
