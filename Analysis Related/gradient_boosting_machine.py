import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.utils.class_weight import compute_sample_weight
from imblearn.pipeline import Pipeline
from sklearn.metrics import make_scorer
import joblib

# Load the labeled data
data_path = 'processed_airdrops_data_latest_ITP1_updated_with_temp_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')
'Requirement_Count', 'Guide_Length'
# Split the data into features and target
X = data.drop(['Title', 'is_scam'], axis=1)  # Assuming 'Title' is not used for prediction
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# # #Applying SMOTE
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# # #Apply ADASYN to the training data
# adasyn = ADASYN(random_state=42)
# X_train_ada, y_train_ada = adasyn.fit_resample(X_train, y_train)

# sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

# weight_for_0 = 1  # weight for majority class
# weight_for_1 = 1842 / 1001  # weight for minority class, more heavily weighted
# sample_weights = compute_sample_weight(
#     class_weight={0: weight_for_0, 1: weight_for_1},
#     y=y_train
# )

# # Calculate class weights based on the new distribution after SMOTE
# total_samples = len(y_train_smote)  # Total number of samples after SMOTE
# num_classes = 2
# count_class_0 = sum(y_train_smote == 0)  # Number of samples in majority class after SMOTE
# count_class_1 = sum(y_train_smote == 1)  # Number of samples in minority class after SMOTE

# # Using direct ratio for explicit weights
# weight_for_0 = 1  # Normalized weight for majority class
# weight_for_1 = count_class_0 / count_class_1  # Explicit weight for minority class based on their ratio

# class_weights = {0: weight_for_0, 1: weight_for_1}
# sample_weights = compute_sample_weight(class_weight={0: weight_for_0, 1: weight_for_1}, y=y_train_smote)

# # Calculate class weights based on the new distribution after ADASYN
# total_samples = len(y_train_ada)
# num_classes = 2
# count_class_0 = sum(y_train_ada == 0)
# count_class_1 = sum(y_train_ada == 1)

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}
# sample_weights = compute_sample_weight(class_weight={0: weight_for_0, 1: weight_for_1}, y=y_train_ada)

# # Define the parameter grid
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_features': ['auto', 'sqrt', 'log2'],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# # Setup GridSearchCV
# grid = GridSearchCV(
#     estimator=GradientBoostingClassifier(random_state=42),
#     param_grid=param_grid,
#     scoring=None,  # Can use multiple metrics or change this as needed
#     cv=3,  # Number of folds in cross-validation
#     verbose=2,
#     n_jobs=-1  # Use all processors
# )


# # Define the parameter grid
# param_grid = {
#     'classifier__n_estimators': [100, 200, 300],
#     'classifier__max_features': ['auto', 'sqrt', 'log2'],
#     'classifier__max_depth': [None, 10, 20, 30],
#     'classifier__min_samples_split': [2, 5, 10],
#     'classifier__min_samples_leaf': [1, 2, 4]
# }

# pipeline = Pipeline([
#     ('adasyn', ADASYN(random_state=42)),
#     ('classifier', GradientBoostingClassifier(random_state=42))
# ])

# # Setup GridSearchCV
# grid = GridSearchCV(
#     estimator=pipeline,
#     param_grid=param_grid,
#     scoring=None,  # Can use multiple metrics or change this as needed
#     cv=3,  # Number of folds in cross-validation
#     verbose=2,
#     n_jobs=-1  # Use all processors
# )


# # Fit GridSearchCV
# grid.fit(X_train, y_train)

# # Get the best model
# gbm_model = grid.best_estimator_

# # # Predictions on the test set using the best model
# gbm_pred = gbm_model.predict(X_test)


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

# Save the trained logistic regression model
model_filename = 'gradient_boosting_model_6_features.joblib'
joblib.dump(gbm_model, model_filename)
print(f"Model saved to {model_filename}")

# Print evaluation results
print("Gradient Boosting Results:")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"F1-score: {f1:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

# Optionally, predict probabilities for the ROC curve or other analysis
# gbm_probs = gbm_model.predict_proba(X_test)[:, 1]
