import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.utils.class_weight import compute_sample_weight
from imblearn.over_sampling import SMOTE, ADASYN
import joblib
from imblearn.pipeline import Pipeline 

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

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# # Applying SMOTE
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# # Apply ADASYN to the training data
# adasyn = ADASYN(random_state=42)
# X_train_ada, y_train_ada = adasyn.fit_resample(X_train, y_train)

# sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)

# total_samples = 1842 + 1001
# num_classes = 2
# count_class_0 = 1842
# count_class_1 = 1001

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)
# class_weights = {0: weight_for_0, 1: weight_for_1}

# weight_for_0 = 1  # weight for majority class
# weight_for_1 = 1842 / 1001  # weight for minority class, more heavily weighted
# sample_weights = compute_sample_weight(
#     class_weight={0: weight_for_0, 1: weight_for_1},
#     y=y_train
# )

# total_samples = len(y_train_smote)  # Total number of samples after SMOTE
# num_classes = 2
# count_class_0 = sum(y_train_smote == 0)  # Number of samples in majority class after SMOTE
# count_class_1 = sum(y_train_smote == 1)  # Number of samples in minority class after SMOTE

# # Using direct ratio for explicit weights
# weight_for_0 = 1  # Normalized weight for majority class
# weight_for_1 = count_class_0 / count_class_1  # Explicit weight for minority class based on their ratio

# class_weights = {0: weight_for_0, 1: weight_for_1}
# sample_weights = compute_sample_weight(class_weight={0: weight_for_0, 1: weight_for_1}, y=y_train_smote)

# total_samples = len(y_train_ada)
# num_classes = 2
# count_class_0 = sum(y_train_ada == 0)
# count_class_1 = sum(y_train_ada == 1)

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}
# sample_weights = compute_sample_weight(class_weight={0: weight_for_0, 1: weight_for_1}, y=y_train_ada)

# param_grid_lr = {
#     'C': [0.01, 0.1, 1, 10, 100],
#     'solver': ['liblinear', 'saga']
# }

# param_grid_rf = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [None, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# param_grid_gbm = {
#     'n_estimators': [100, 200, 300],
#     'learning_rate': [0.01, 0.1, 0.2],
#     'max_depth': [3, 5, 8]
# }

# grid_lr = GridSearchCV(LogisticRegression(random_state=42), param_grid_lr, scoring=None, cv=3)
# grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid_rf, scoring=None, cv=3)
# grid_gbm = GridSearchCV(GradientBoostingClassifier(random_state=42), param_grid_gbm, scoring=None, cv=3)


# # #Setup parameter grids with prefixes
# param_grid_lr = {
#     'classifier__C': [0.01, 0.1, 1, 10, 100],
#     'classifier__solver': ['liblinear', 'saga']
# }

# param_grid_rf = {
#     'classifier__n_estimators': [100, 200, 300],
#     'classifier__max_depth': [None, 10, 20],
#     'classifier__min_samples_split': [2, 5, 10],
#     'classifier__min_samples_leaf': [1, 2, 4]
# }

# param_grid_gbm = {
#     'classifier__n_estimators': [100, 200, 300],
#     'classifier__learning_rate': [0.01, 0.1, 0.2],
#     'classifier__max_depth': [3, 5, 8]
# }

# lr_pipeline = Pipeline([
#     ('smote', SMOTE(random_state=42)),
#     ('classifier', LogisticRegression())
# ])

# rf_pipeline = Pipeline([
#     ('smote', SMOTE(random_state=42)),
#     ('classifier', RandomForestClassifier(random_state=42))
# ])

# gbm_pipeline = Pipeline([
#     ('smote', SMOTE(random_state=42)),
#     ('classifier', GradientBoostingClassifier(random_state=42))
# ])

# # Setup GridSearchCV for each pipeline
# grid_lr = GridSearchCV(lr_pipeline, param_grid_lr, scoring=None, cv=3, verbose=2)
# grid_rf = GridSearchCV(rf_pipeline, param_grid_rf, scoring=None, cv=3, verbose=2)
# grid_gbm = GridSearchCV(gbm_pipeline, param_grid_gbm, scoring=None, cv=3, verbose=2)

# grid_lr.fit(X_train, y_train)
# grid_rf.fit(X_train, y_train)
# grid_gbm.fit(X_train, y_train)

# # Get the best estimator
# lr_model = grid_lr.best_estimator_
# rf_model = grid_rf.best_estimator_
# gbm_model = grid_gbm.best_estimator_

# # Predict probabilities on the test set
# lr_probs = lr_model.predict_proba(X_test)[:, 1]
# rf_probs = rf_model.predict_proba(X_test)[:, 1]
# gbm_probs = gbm_model.predict_proba(X_test)[:, 1]

# Initialize and train the logistic regression model
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Initialize and train the random forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Initialize and train the gradient boosting model
gbm_model = GradientBoostingClassifier(random_state=42)
gbm_model.fit(X_train, y_train)

# sample_weight=sample_weights
# Predict probabilities on the test set
lr_probs = lr_model.predict_proba(X_test)[:, 1]
rf_probs = rf_model.predict_proba(X_test)[:, 1]
gbm_probs = gbm_model.predict_proba(X_test)[:, 1]

# Combine the probabilities: Let's say we trust LR a bit less, we give it a weight of 0.4 and RF a weight of 0.6
combined_probs = (0.3 * lr_probs + 0.4 * rf_probs + 0.3 * gbm_probs)
# Essentially, this line transforms probability estimates into definitive class labels based on a specified threshold, which is typically 0.5 in binary classification tasks.
combined_pred = [1 if prob > 0.5 else 0 for prob in combined_probs]

# Save the trained logistic regression model
model_filename = 'logistic_regression_model_6_features.joblib'
joblib.dump(lr_model, model_filename)
print(f"Model saved to {model_filename}")

# Save the trained random forest model
model_filename = 'random_forest_model_6_features.joblib'
joblib.dump(rf_model, model_filename)
print(f"Model saved to {model_filename}")

# Save the trained gradient boosting model
model_filename = 'gradient_boosting_model_6_features.joblib'
joblib.dump(gbm_model, model_filename)
print(f"Model saved to {model_filename}")

# Print the scores
print("Logistic Regression & Random Forest & Gradient Boosting Machine")
print(f"Accuracy: {accuracy_score(y_test, combined_pred)*100:.2f}%")
print(f"F1-score: {f1_score(y_test, combined_pred):.2f}")
print(f"Precision: {precision_score(y_test, combined_pred):.2f}")
print(f"Recall: {recall_score(y_test, combined_pred):.2f}")

# Predict and combine probabilities on the entire dataset for output consistency
# data['scam_possibility'] = (0.4 * lr_model.predict_proba(X_scaled)[:, 1] + 0.6 * rf_model.predict_proba(X_scaled)[:, 1] + 0.3 * gbm_model.predict_proba(X_scaled)[:, 1]).round(2)

# Save the updated dataframe to a new file
# output_path = 'processed_airdrops_data_with_scam_labelled_probabilities.csv'
# data.to_csv(output_path, index=False)
# print(f"Updated data with scam possibility saved to {output_path}.")