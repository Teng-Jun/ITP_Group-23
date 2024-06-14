import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Load the labeled data
data_path = 'processed_airdrops_data_with_scam_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')

'Requirement_Count', 'Guide_Length'
# Split the data into features and target
X = data.drop(['Title', 'is_scam', 'Requirement_Count', 'Guide_Length'], axis=1)  # Assuming 'Title' is not used for prediction
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Initialize and train the logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Initialize and train the random forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Predict probabilities on the test set
lr_probs = lr_model.predict_proba(X_test)[:, 1]
rf_probs = rf_model.predict_proba(X_test)[:, 1]

# Combine the probabilities: Let's say we trust LR a bit less, we give it a weight of 0.4 and RF a weight of 0.6
combined_probs = (0.4 * lr_probs + 0.6 * rf_probs)
# Essentially, this line transforms probability estimates into definitive class labels based on a specified threshold, which is typically 0.5 in binary classification tasks.
combined_pred = [1 if prob > 0.5 else 0 for prob in combined_probs]

# Print the scores
print(f"Accuracy: {accuracy_score(y_test, combined_pred)*100:.2f}%")
print(f"F1-score: {f1_score(y_test, combined_pred):.2f}")
print(f"Precision: {precision_score(y_test, combined_pred):.2f}")
print(f"Recall: {recall_score(y_test, combined_pred):.2f}")

# Predict and combine probabilities on the entire dataset for output consistency
data['scam_possibility'] = (0.4 * lr_model.predict_proba(X_scaled)[:, 1] + 0.6 * rf_model.predict_proba(X_scaled)[:, 1]).round(2)

# Save the updated dataframe to a new file
output_path = 'processed_airdrops_data_with_scam_labelled_probabilities.csv'
data.to_csv(output_path, index=False)
print(f"Updated data with scam possibility saved to {output_path}.")