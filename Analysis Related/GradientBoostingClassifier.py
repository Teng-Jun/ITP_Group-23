import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
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
X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Initialize and train the Random Forest classifier
gbm_model = GradientBoostingClassifier(random_state=42)
gbm_model.fit(X_train, y_train)

# Predictions on the test set
gbm_pred = gbm_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, gbm_pred)
f1 = f1_score(y_test, gbm_pred)
precision = precision_score(y_test, gbm_pred)
recall = recall_score(y_test, gbm_pred)

# Print evaluation results
print("Gradient Boosting Results:")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"F1-score: {f1:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

# Optionally, predict probabilities for the ROC curve or other analysis
gbm_probs = gbm_model.predict_proba(X_test)[:, 1]
