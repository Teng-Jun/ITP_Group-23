import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, make_scorer
from sklearn.utils.class_weight import compute_sample_weight
import joblib

# total_samples = 1842 + 1001
# num_classes = 2
# count_class_0 = 1842
# count_class_1 = 1001

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}

# Load the labeled data
data_path = 'processed_airdrops_data_with_more_scam_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')

'Requirement_Count', 'Guide_Length'
# Split the data into features and target
X = data.drop(['Title', 'is_scam'], axis=1)  # Assuming 'Title' is not used for prediction
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

scaler_filename = 'scaler.joblib'
joblib.dump(scaler, scaler_filename)
print(f"Scaler saved to {scaler_filename}")


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Apply SMOTE to the training data
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Apply ADASYN to the training data
# adasyn = ADASYN(random_state=42)
# X_train_ada, y_train_ada = adasyn.fit_resample(X_train, y_train)

# Define the parameter grid for Logistic Regression
param_grid_lr = {
    'C': [0.001, 0.01, 0.1, 1, 10],  # Regularization strength
    'solver': ['liblinear', 'saga'],  # Optimization algorithms
    'penalty': ['l1', 'l2']  # Norms for penalization
}

# Initialize GridSearchCV
grid_lr = GridSearchCV(
    LogisticRegression(max_iter=1000),
    param_grid_lr,
    scoring=None,  # You can also use a custom scorer dictionary or multiple scorers
    cv=5,
    verbose=1,
    n_jobs=-1  # Use all available cores
)

# Fit GridSearchCV on the training data
grid_lr.fit(X_train, y_train)

# Extract the best model
lr_model = grid_lr.best_estimator_

# Calculate class weights based on the imbalance
# total_samples = len(y_train_smote)
# num_classes = 2
# count_class_0 = sum(y_train_smote == 0)
# count_class_1 = sum(y_train_smote == 1)

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}

# Calculate class weights based on the new distribution after ADASYN
# total_samples = len(y_train_ada)
# num_classes = 2
# count_class_0 = sum(y_train_ada == 0)
# count_class_1 = sum(y_train_ada == 1)

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}

# Initialize and train the logistic regression model
# lr_model = LogisticRegression()
# lr_model.fit(X_train, y_train)

# Predictions on the test set
# The predict method in LogisticRegression (and other classifiers in scikit-learn) internally uses a default threshold of 0.5 to convert the model's output probabilities into class labels. When the predicted probability is greater than or equal to 0.5, the method assigns a class label of 1; otherwise, it assigns a class label of 0
# lr_pred = lr_model.predict(X_test)

# Predictions on the test set
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
print("Best parameters found by GridSearchCV:", grid_lr.best_params_)

# Save the trained logistic regression model
model_filename = 'logistic_regression_model_best_parameter.joblib'
# joblib.dump(lr_model, model_filename)
joblib.dump(lr_model, model_filename)
print(f"Model saved to {model_filename}")

# # Predict and combine probabilities on the entire dataset for output consistency
# # data['scam_possibility'] = lr_model.predict_proba(X_scaled)[:, 1]
# data['scam_possibility'] = lr_model.predict_proba(X_scaled)[:, 1]
# data['scam_possibility'] = data['scam_possibility'].round(2)

# # Save the updated dataframe to a new file
# output_path = 'processed_airdrops_data_with_more_scam_labelled_probabilities.csv'
# data.to_csv(output_path, index=False)
# print(f"Updated data with scam possibility saved to {output_path}.")


