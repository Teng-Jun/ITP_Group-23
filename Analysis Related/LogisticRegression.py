import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Load the labeled data
data_path = 'processed_airdrops_data_with_scam.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')

# Split the data into features and target
X = data.drop(['Title', 'is_scam'], axis=1)  # Assuming 'Title' is not used for prediction
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Initialize and train the logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predictions on the test set
# The predict method in LogisticRegression (and other classifiers in scikit-learn) internally uses a default threshold of 0.5 to convert the model's output probabilities into class labels. When the predicted probability is greater than or equal to 0.5, the method assigns a class label of 1; otherwise, it assigns a class label of 0
y_pred = model.predict(X_test)

# Calculate accuracy, F1-score, precision, and recall
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

# Print the scores
print(f"Model accuracy: {accuracy*100:.2f}%")
print(f"Model F1-score: {f1:.2f}")
print(f"Model Precision: {precision:.2f}")
print(f"Model Recall: {recall:.2f}")

# Predict probabilities on the entire dataset (for output consistency)
data['scam_possibility'] = model.predict_proba(X_scaled)[:, 1]
data['scam_possibility'] = data['scam_possibility'].round(2)

# Save the updated dataframe to a new file
output_path = 'processed_airdrops_data_with_scam_labelled_probability.csv'
data.to_csv(output_path, index=False)
print(f"Updated data with scam possibility saved to {output_path}.")