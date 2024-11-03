import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def evaluate_model(ground_truth_path, predictions_path, model_name, threshold=0.3):
    # Load data
    ground_truth = pd.read_csv(ground_truth_path)
    predictions = pd.read_csv(predictions_path)
    
    # Merge datasets
    df = pd.merge(ground_truth, predictions, left_on='Token Name', right_on='airdrop_name', how='inner')

    # Generate predictions
    y_pred = (df['scam_probability'] > threshold).astype(int)  # Use specified threshold
    y_true = df['Is Scam'].astype(int)

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Print results
    print(f"{model_name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    
    # Visualize the confusion matrix
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Non-Scam', 'Scam'], 
                yticklabels=['Non-Scam', 'Scam'])
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title(f'Confusion Matrix for {model_name}')
    plt.show()

# Run evaluation for each model with a threshold
ground_truth_path = "ground_truth_labels.csv"
model_files = {
    'BERT': 'bert_airdrop_sentiment_results.csv',
    'Custom Dict': 'custom_dictionary_airdrop_sentiment_results.csv',
    'RoBERTa': 'roberta_airdrop_sentiment_combined_results.csv',
    'TextBlob': 'textblob_airdrop_sentiment_results.csv',
    'VADER': 'vader_airdrop_sentiment_results_1.csv'
}

# Test with different thresholds
for model_name, file_path in model_files.items():
    for threshold in [0.1, 0.2, 0.3, 0.4, 0.5]:
        print(f"Evaluating {model_name} with threshold {threshold}")
        evaluate_model(ground_truth_path, file_path, model_name, threshold)
