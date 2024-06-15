import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

# Load the labeled data
data_path = 'processed_airdrops_data_with_scam_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')

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

# Predictions on the test set
# The predict method in LogisticRegression (and other classifiers in scikit-learn) internally uses a default threshold of 0.5 to convert the model's output probabilities into class labels. When the predicted probability is greater than or equal to 0.5, the method assigns a class label of 1; otherwise, it assigns a class label of 0
lr_pred = lr_model.predict(X_test)

# Calculate accuracy, F1-score, precision, and recall
accuracy = accuracy_score(y_test, lr_pred)
f1 = f1_score(y_test, lr_pred)
precision = precision_score(y_test, lr_pred)
recall = recall_score(y_test, lr_pred)

# Print the scores
print("Logistic Regression Results:")
print(f"Model accuracy: {accuracy*100:.2f}%")
print(f"Model F1-score: {f1:.2f}")
print(f"Model Precision: {precision:.2f}")
print(f"Model Recall: {recall:.2f}")

lr_probs = lr_model.predict_proba(X_test)[:, 1]



