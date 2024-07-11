import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.utils.class_weight import compute_sample_weight
from imblearn.over_sampling import SMOTE, ADASYN

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

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Applying SMOTE
# smote = SMOTE(random_state=42)
# X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# Apply ADASYN to the training data
adasyn = ADASYN(random_state=42)
X_train_ada, y_train_ada = adasyn.fit_resample(X_train, y_train)

# sample_weights = compute_sample_weight(class_weight='balanced', y=y_train_ada)

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

total_samples = len(y_train_ada)
num_classes = 2
count_class_0 = sum(y_train_ada == 0)
count_class_1 = sum(y_train_ada == 1)

weight_for_0 = total_samples / (num_classes * count_class_0)
weight_for_1 = total_samples / (num_classes * count_class_1)

class_weights = {0: weight_for_0, 1: weight_for_1}
sample_weights = compute_sample_weight(class_weight={0: weight_for_0, 1: weight_for_1}, y=y_train_ada)

# Initialize and train the logistic regression model
lr_model = LogisticRegression(class_weight=class_weights)
lr_model.fit(X_train_ada, y_train_ada)

# Initialize and train the random forest model
rf_model = RandomForestClassifier(random_state=42, class_weight=class_weights)
rf_model.fit(X_train_ada, y_train_ada)

# Initialize and train the gradient boosting model
gbm_model = GradientBoostingClassifier(random_state=42)
gbm_model.fit(X_train_ada, y_train_ada, sample_weight=sample_weights)
# , sample_weight=sample_weights
# Predict probabilities on the test set
lr_probs = lr_model.predict_proba(X_test)[:, 1]
rf_probs = rf_model.predict_proba(X_test)[:, 1]
gbm_probs = gbm_model.predict_proba(X_test)[:, 1]

# Combine the probabilities: Let's say we trust LR a bit less, we give it a weight of 0.4 and RF a weight of 0.6
combined_probs = (0.3 * lr_probs + 0.4 * rf_probs + + 0.3 * gbm_probs)
# Essentially, this line transforms probability estimates into definitive class labels based on a specified threshold, which is typically 0.5 in binary classification tasks.
combined_pred = [1 if prob > 0.5 else 0 for prob in combined_probs]

# Print the scores
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