import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, roc_auc_score
from imblearn.combine import SMOTETomek
import xgboost as xgb
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
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

# Models for boosting
boosting_models = {
    'XGBoost': xgb.XGBClassifier(
        learning_rate=0.01,
        n_estimators=200,
        max_depth=4,
        min_child_weight=2,
        gamma=1,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=5,
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

# Evaluate boosted models for each sentiment model
results = []
scaler = StandardScaler()

for sentiment_model_name, model_data in all_data.groupby('model'):
    print(f"Evaluating boosted models for {sentiment_model_name}...")

    # Define features and labels
    X = model_data[
        ['positive', 'neutral', 'negative', 'total_words', 'total_upvotes',
         'comment_count', 'average_comment_length']
    ]
    y = model_data['is_scam']

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Scale features
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Apply SMOTETomek
    smote_tomek = SMOTETomek(random_state=42)
    X_train_resampled, y_train_resampled = smote_tomek.fit_resample(X_train_scaled, y_train)

    for boosting_model_name, boosting_model in boosting_models.items():
        print(f"Training {boosting_model_name} for {sentiment_model_name}...")

        # Train the model
        boosting_model.fit(X_train_resampled, y_train_resampled)

        # Predict on the test set
        y_pred = boosting_model.predict(X_test_scaled)
        y_pred_proba = boosting_model.predict_proba(X_test_scaled)[:, 1]

        # Calculate metrics
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        accuracy = accuracy_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)

        results.append({
            'Sentiment Model': sentiment_model_name,
            'Boosting Model': boosting_model_name,
            'Precision': precision,
            'Recall': recall,
            'F1': f1,
            'Accuracy': accuracy,
            'ROC AUC': roc_auc
        })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to CSV
results_df.to_csv('results_sentiment_models_boosted/test_set_boosted_comparison_results.csv', index=False)

# Define x_positions based on the number of sentiment models
sentiment_models = results_df['Sentiment Model'].unique()
num_models = len(sentiment_models)
x_positions = np.arange(num_models)

# Plot the comparison for all metrics
metrics = ['Precision', 'Recall', 'F1', 'Accuracy', 'ROC AUC']
colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff5a5f']
bar_width = 0.15

# Create subplots for each metric
plt.figure(figsize=(20, 15))

for i, metric in enumerate(metrics):
    plt.subplot(3, 2, i + 1)
    
    for j, boosting_model in enumerate(results_df['Boosting Model'].unique()):
        model_results = results_df[results_df['Boosting Model'] == boosting_model]
        plt.bar(
            x_positions + j * bar_width,
            model_results[metric],
            bar_width,
            label=boosting_model if i == 0 else None,  # Only label the first subplot
            alpha=0.8,
            color=colors[j % len(colors)]
        )
    
    # Customize each subplot
    plt.xlabel('Sentiment Models')
    plt.ylabel(metric)
    plt.title(f'Comparison of {metric} Across Sentiment Models and Boosting Methods')
    plt.xticks(x_positions + bar_width * (len(results_df['Boosting Model'].unique()) - 1) / 2, sentiment_models, rotation=45, ha='right')
    plt.ylim(0, 1)  # All metrics are percentages, so limit to 1
    
    if i == 0:  # Add legend only once
        plt.legend()

# Adjust layout and save
plt.tight_layout()
plt.savefig('results_sentiment_models_boosted/all_metrics_comparison_plot.png', dpi=300, bbox_inches='tight')
print("All metrics comparison plot saved as 'results_sentiment_models_boosted/all_metrics_comparison_plot.png'")

# Show the combined plot
plt.show()