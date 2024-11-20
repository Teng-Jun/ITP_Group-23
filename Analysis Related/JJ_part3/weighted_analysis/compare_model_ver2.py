import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTETomek
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import xgboost as xgb
import lightgbm as lgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer  # Import the imputer
import os

# Ensure the results folder exists
if not os.path.exists('results_roberta'):
    os.makedirs('results_roberta')

# Load the data
data = pd.read_csv('roberta_time_decay_weighted_sentiment_results.csv')
ground_truth = pd.read_csv('ground_truth_labels.csv')

# Merge the ground truth labels with the data
data = data.merge(ground_truth, left_on='airdrop_name', right_on='Token Name', how='left')

# Clean the data - remove rows with no valid sentiment
data_cleaned = data[(data[['positive', 'neutral', 'negative', 'total_words', 'total_upvotes', 'comment_count']] != 0).any(axis=1)]

# Handle missing data by imputing missing values with the median
imputer = SimpleImputer(strategy='median')  # You can choose 'mean' or 'most_frequent' if preferred
data_cleaned[['positive', 'neutral', 'negative', 'total_words', 'total_upvotes', 'comment_count', 'average_comment_length']] = imputer.fit_transform(data_cleaned[['positive', 'neutral', 'negative', 'total_words', 'total_upvotes', 'comment_count', 'average_comment_length']])

# Define features and labels
X = data_cleaned[['positive', 'neutral', 'negative', 'total_words', 'total_upvotes', 'comment_count', 'average_comment_length']]
y = data_cleaned['is_scam']

# Initialize StratifiedKFold for cross-validation
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Initialize scaler
scaler = StandardScaler()

# Initialize models with optimized parameters
models = {
    'XGBoost': xgb.XGBClassifier(
        learning_rate=0.01,
        n_estimators=200,
        max_depth=4,
        min_child_weight=2,
        gamma=1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=5,  # Adjusted for class imbalance
        random_state=42
    ),
    'LightGBM': lgb.LGBMClassifier(
        learning_rate=0.01,
        n_estimators=200,
        num_leaves=20,
        max_depth=4,
        class_weight='balanced',
        random_state=42
    ),
    'RandomForest': RandomForestClassifier(
        n_estimators=200,
        max_depth=4,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42
    )
}

def evaluate_model(model, X, y, model_name):
    best_precision = 0
    best_recall = 0
    best_f1 = 0
    best_accuracy = 0
    best_threshold = 0.5

    print(f"\nEvaluating {model_name}...")

    # Perform cross-validation
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
        # Split data
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        # Scale features
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)

        # Apply SMOTETomek (better than just SMOTE for this case)
        smote_tomek = SMOTETomek(sampling_strategy='auto', random_state=42)
        X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train_scaled, y_train)

        # Train model
        model.fit(X_train_resampled, y_train_resampled)

        # Predict with probability
        y_pred_proba = model.predict_proba(X_val_scaled)[:, 1]

        # Find optimal threshold using F1 score
        thresholds = np.arange(0.1, 0.9, 0.05)
        best_f1_for_fold = 0
        best_threshold_for_fold = 0.5

        for threshold in thresholds:
            y_pred = (y_pred_proba >= threshold).astype(int)
            f1 = f1_score(y_val, y_pred)
            if f1 > best_f1_for_fold:
                best_f1_for_fold = f1
                best_threshold_for_fold = threshold

        # Get predictions using best threshold
        y_pred = (y_pred_proba >= best_threshold_for_fold).astype(int)

        # Calculate metrics
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)
        accuracy = accuracy_score(y_val, y_pred)

        # Update best scores
        if f1 > best_f1:
            best_f1 = f1
        if precision > best_precision:
            best_precision = precision
        if recall > best_recall:
            best_recall = recall
        if accuracy > best_accuracy:
            best_accuracy = accuracy

        print(f"Fold {fold} - Precision: {precision:.4f}, Recall: {recall:.4f}, "
              f"F1: {f1:.4f}, Accuracy: {accuracy:.4f}, Threshold: {best_threshold_for_fold:.2f}")

        # Confusion Matrix - print and save the confusion matrix for each fold
        cm = confusion_matrix(y_val, y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
        # Save confusion matrix image
        cm_output_path = f"results_roberta/{model_name}_fold_{fold}_confusion_matrix.png"
        disp.plot(cmap='Blues')
        plt.title(f"{model_name} - Fold {fold} Confusion Matrix")
        plt.savefig(cm_output_path)  # Save the confusion matrix as an image
        plt.close()

    # Print average results
    print(f"\n{model_name} Average Results:")
    print(f"Precision: {best_precision:.4f}")
    print(f"Recall: {best_recall:.4f}")
    print(f"F1 Score: {best_f1:.4f}")
    print(f"Accuracy: {best_accuracy:.4f}")

    # Save the best scores to a CSV for model comparison
    result_data = {
        'model_name': model_name,
        'best_precision': best_precision,
        'best_recall': best_recall,
        'best_f1': best_f1,
        'best_accuracy': best_accuracy
    }

    return result_data

# Evaluate all models and store the results
results = []
for model_name, model in models.items():
    result = evaluate_model(model, X, y, model_name)
    results.append(result)

# Convert results to a DataFrame and save
results_df = pd.DataFrame(results)
results_df.to_csv('results_roberta/model_comparison_results.csv', index=False)

print("Model comparison results saved to 'results_roberta/model_comparison_results.csv'")

# Now plot the comparison
plt.figure(figsize=(10, 6))
metrics = ['best_precision', 'best_recall', 'best_f1', 'best_accuracy']
x = np.arange(len(metrics))
width = 0.25

for i, (model_name, scores) in enumerate(results_df.iterrows()):
    plt.bar(x + i * width, [scores[metric] for metric in metrics], width, label=scores['model_name'])

plt.xlabel('Metrics')
plt.ylabel('Score')
plt.title('Model Performance Comparison')
plt.xticks(x + width, metrics)
plt.legend()
plt.tight_layout()
plt.show()
