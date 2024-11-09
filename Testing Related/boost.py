import pandas as pd
from catboost import CatBoostClassifier, Pool
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

# Convert training data into Pool format for CatBoost (not strictly required but recommended for CatBoost)
train_pool = Pool(X_train, y_train)

# Initialize and train the CatBoost classifier with basic parameters
catboost_model = CatBoostClassifier(
    iterations=500,         # Number of boosting iterations
    depth=6,                # Depth of the trees
    learning_rate=0.1,      # Learning rate
    random_seed=42,         # Random seed for reproducibility
    eval_metric='F1',       # Metric used to evaluate the model
    class_weights=[1, len(y_train) / sum(y_train == 1)]  # Optional class balancing
)

# Fit the model
catboost_model.fit(train_pool, verbose=100)

# Save the trained CatBoost model
model_filename = 'catboost_model.joblib'
joblib.dump(catboost_model, model_filename)
print(f"Model saved to {model_filename}")

# Predict probabilities and labels on the test set
catboost_probs = catboost_model.predict_proba(X_test)[:, 1]
catboost_pred = (catboost_probs > 0.5).astype(int)  # Apply threshold for classification

# Evaluate the model
accuracy = accuracy_score(y_test, catboost_pred)
f1 = f1_score(y_test, catboost_pred)
precision = precision_score(y_test, catboost_pred)
recall = recall_score(y_test, catboost_pred)

# Print evaluation metrics
print("CatBoost Results:")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"F1-score: {f1:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

# # Optional: Save probabilities in the dataset for analysis
# data['scam_possibility'] = catboost_model.predict_proba(scaler.transform(X))[:, 1].round(2)
# output_path = 'processed_airdrops_data_with_catboost_probabilities.csv'
# data.to_csv(output_path, index=False)
# print(f"Updated data with scam probabilities saved to {output_path}.")
