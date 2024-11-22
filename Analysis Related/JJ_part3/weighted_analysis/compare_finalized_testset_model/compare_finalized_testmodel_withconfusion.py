import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
from imblearn.combine import SMOTETomek
import lightgbm as lgb
import matplotlib.pyplot as plt
import os

# Ensure results folder exists
if not os.path.exists('results_sentiment_models_boosted'):
    os.makedirs('results_sentiment_models_boosted')

# Load data for all sentiment models
data_roberta = pd.read_csv('roberta_time_decay_weighted_sentiment_results.csv')
data_bert = pd.read_csv('bert_time_decay_weighted_sentiment_results_latest.csv')
data_custom = pd.read_csv('customdicwords_time_decay_weighted_sentiment_results.csv')
data_vader = pd.read_csv('vader_time_decay_weighted_sentiment_results_2.csv')
data_textblob = pd.read_csv('textblob_time_decay_weighted_sentiment_results.csv')
ground_truth = pd.read_csv('ground_truth_labels.csv')

# Prepare and merge data for each sentiment model
def prepare_data(model_data, model_name):
    merged = model_data.merge(ground_truth, left_on='airdrop_name', right_on='Token Name', how='left')
    features = [
        'positive', 'neutral', 'negative', 'total_words', 'total_upvotes',
        'comment_count', 'average_comment_length'
    ]
    merged = merged[(merged[features] != 0).any(axis=1)]
    merged['model'] = model_name
    return merged

# Prepare data for each sentiment model
data_roberta = prepare_data(data_roberta, 'RoBERTa')
data_bert = prepare_data(data_bert, 'BERT')
data_custom = prepare_data(data_custom, 'Custom Dictionary')
data_vader = prepare_data(data_vader, 'VADER')
data_textblob = prepare_data(data_textblob, 'TextBlob')

# Combine all data
all_data = pd.concat([data_roberta, data_bert, data_custom, data_vader, data_textblob])

# LightGBM model for boosting
lightgbm_model = lgb.LGBMClassifier(
    learning_rate=0.01,
    n_estimators=200,
    num_leaves=20,
    max_depth=4,
    class_weight='balanced',
    random_state=42
)

# Evaluate LightGBM model for each sentiment model
results = []
scaler = StandardScaler()
total_test_samples = 0

for sentiment_model_name, model_data in all_data.groupby('model'):
    print(f"Evaluating LightGBM model for {sentiment_model_name}...")

    # Define features and labels
    X = model_data[
        ['positive', 'neutral', 'negative', 'total_words', 'total_upvotes',
         'comment_count', 'average_comment_length']
    ]
    y = model_data['is_scam']

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Count test samples
    total_test_samples += X_test.shape[0]

    # Scale features
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply SMOTETomek
    smote_tomek = SMOTETomek(random_state=42)
    X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train_scaled, y_train)

    # Train the model
    lightgbm_model.fit(X_train_resampled, y_train_resampled)

    # Predict on the test set
    y_pred = lightgbm_model.predict(X_test_scaled)
    y_pred_proba = lightgbm_model.predict_proba(X_test_scaled)[:, 1]

    # Calculate metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    # Store results
    results.append({
        'Sentiment Model': sentiment_model_name,
        'Precision': precision,
        'Recall': recall,
        'F1': f1,
        'Accuracy': accuracy,
        'ROC AUC': roc_auc
    })

    # Generate and save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap='Blues', values_format='d')
    plt.title(f'Confusion Matrix for LightGBM ({sentiment_model_name})')
    plt.savefig(f'results_sentiment_models_boosted/confusion_matrix_{sentiment_model_name}_LightGBM.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the plot to prevent overlap in the next iteration
    print(f"Confusion matrix saved for LightGBM ({sentiment_model_name})")

# Print total number of test samples
print(f"\nTotal number of test samples used: {total_test_samples}")

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to CSV
results_df.to_csv('results_sentiment_models_boosted/test_set_lightgbm_results.csv', index=False)

print("All LightGBM model evaluation results saved.")
