import pandas as pd
from imblearn.over_sampling import SMOTE, ADASYN
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


# Load the labeled data
data_path = 'processed_airdrops_data_with_more_scam_labelled.csv'
data = pd.read_csv(data_path, encoding='ISO-8859-1')
'Requirement_Count', 'Guide_Length'
# Split the data into features and target
X = data.drop(['Title', 'is_scam', 'Requirement_Count', 'Guide_Length'], axis=1)  # Assuming 'Title' is not used for prediction
y = data['is_scam'].astype(int)

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns, index=X.index)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# total_samples = 1842 + 1001
# num_classes = 2
# count_class_0 = 1842
# count_class_1 = 1001

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}

# Apply SMOTE to the training data
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Apply ADASYN to the training data
adasyn = ADASYN(random_state=42)
X_train_ada, y_train_ada = adasyn.fit_resample(X_train, y_train)

# Calculate class weights based on the imbalance
# total_samples = len(y_train_smote)
# num_classes = 2
# count_class_0 = sum(y_train_smote == 0)
# count_class_1 = sum(y_train_smote == 1)

# weight_for_0 = total_samples / (num_classes * count_class_0)
# weight_for_1 = total_samples / (num_classes * count_class_1)

# class_weights = {0: weight_for_0, 1: weight_for_1}

# Define parameters grid for GridSearchCV
# param_grid = {
#     'n_estimators': [100, 200],
#     'max_depth': [10, 20],
#     'min_samples_split': [5, 10],
#     'min_samples_leaf': [2, 3]
# }

# Calculate class weights based on the new distribution after ADASYN
total_samples = len(y_train_ada)
num_classes = 2
count_class_0 = sum(y_train_ada == 0)
count_class_1 = sum(y_train_ada == 1)

weight_for_0 = total_samples / (num_classes * count_class_0)
weight_for_1 = total_samples / (num_classes * count_class_1)

class_weights = {0: weight_for_0, 1: weight_for_1}

# # Initialize and train the Random Forest clsassifier
rf_model = RandomForestClassifier(random_state=42, class_weight=class_weights)
rf_model.fit(X_train_ada, y_train_ada)

# Set up GridSearchCV
# grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=10, n_jobs=-1, verbose=2, scoring='precision')
# grid_search.fit(X_train_smote, y_train_smote)

# Output the best parameters and best score
# print("Best parameters:", grid_search.best_params_)
# print("Best precision score:", grid_search.best_score_)

# best_rf_model = grid_search.best_estimator_
# rf_pred = best_rf_model.predict(X_test)

# Predictions on the test set
rf_pred = rf_model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, rf_pred)
f1 = f1_score(y_test, rf_pred)
precision = precision_score(y_test, rf_pred)
recall = recall_score(y_test, rf_pred)

# Print evaluation results
print("Random Forest Results:")
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"F1-score: {f1:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")


# Optionally, predict probabilities for the ROC curve or other analysis
# rf_probs = rf_model.predict_proba(X_test)[:, 1]


