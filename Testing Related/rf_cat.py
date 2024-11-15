import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import joblib

# Load the data
data_path = 'processed_airdrops_data_latest_more_fake_data_6_features_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')

# Define features and target
X = data.drop(['Title', 'is_scam'], axis=1)
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Train CatBoost model
catboost_model = CatBoostClassifier(
    iterations=500,
    depth=6,
    learning_rate=0.1,
    random_seed=42,
    eval_metric='F1',
    class_weights=[1, len(y_train) / sum(y_train == 1)]  # Optional class balancing
)
catboost_model.fit(X_train, y_train, verbose=100)

# Save CatBoost model
joblib.dump(catboost_model, 'catboost_model.joblib')

# Train Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Save Random Forest model
joblib.dump(rf_model, 'random_forest_model.joblib')

# Predict probabilities on the test set
catboost_probs = catboost_model.predict_proba(X_test)[:, 1]
rf_probs = rf_model.predict_proba(X_test)[:, 1]

# Combine probabilities using a weighted average
# Adjust weights as needed based on individual model performance
combined_probs = 0.5 * catboost_probs + 0.5 * rf_probs
combined_pred = (combined_probs > 0.5).astype(int)

# Evaluate combined predictions
accuracy = accuracy_score(y_test, combined_pred)
f1 = f1_score(y_test, combined_pred)
precision = precision_score(y_test, combined_pred)
recall = recall_score(y_test, combined_pred)

# Print evaluation metrics
print("Combined Model Results:")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"F1-score: {f1:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

# Optional: Save probabilities in the dataset for analysis
data['scam_possibility'] = 0.6 * catboost_model.predict_proba(X_scaled)[:, 1] + 0.4 * rf_model.predict_proba(X_scaled)[:, 1]
data['scam_possibility'] = data['scam_possibility'].round(2)
output_path = 'processed_airdrops_data_with_combined_probabilities.csv'
data.to_csv(output_path, index=False)
print(f"Updated data with combined probabilities saved to {output_path}.")
