import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, fbeta_score
)
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Tuple
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE

class ModelEvaluator:
    def __init__(self, ground_truth_path: str, predictions_paths: Dict[str, str]):
        self.ground_truth = pd.read_csv(ground_truth_path)
        self.merged_data = {}

        for model_name, path in predictions_paths.items():
            preds = pd.read_csv(path)
            merged = pd.merge(self.ground_truth, preds, 
                              left_on='Token Name', 
                              right_on='airdrop_name', 
                              how='inner')
            self.merged_data[model_name] = merged

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features for model training."""
        features = df.copy()
        
        # Basic probability features
        features['scam_probability'] = pd.to_numeric(features['scam_probability'], errors='coerce')
        features['scam_probability'] = features['scam_probability'].fillna(features['scam_probability'].mean())
        features['scam_probability'] = features['scam_probability'].clip(0, 1)

        # Transform features
        features['prob_log'] = np.log1p(features['scam_probability'])
        features['prob_sqrt'] = np.sqrt(features['scam_probability'])
        features['prob_squared'] = features['scam_probability'] ** 2
        
        return features

    def evaluate_threshold(self, model_name: str, threshold: float) -> Tuple[dict, np.ndarray]:
        df = self.merged_data[model_name]
        df = self.create_features(df)

        # Split the dataset
        X = df[['scam_probability', 'prob_log', 'prob_sqrt', 'prob_squared']]
        y = df['Is Scam'].astype(int)

        # Apply SMOTE
        smote = SMOTE(sampling_strategy='minority', random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)

        # Train Random Forest Classifier
        model = RandomForestClassifier(class_weight='balanced', n_estimators=20, random_state=42)  # Reduced n_estimators for quicker tests
        model.fit(X_resampled, y_resampled)

        y_pred_proba = model.predict_proba(X)[:, 1]
        y_pred = (y_pred_proba > threshold).astype(int)

        metrics = {
            'accuracy': accuracy_score(y, y_pred),
            'precision': precision_score(y, y_pred, zero_division=0),
            'recall': recall_score(y, y_pred, zero_division=0),
            'f1': f1_score(y, y_pred, zero_division=0),
            'f2': fbeta_score(y, y_pred, beta=2, zero_division=0)
        }
        
        cm = confusion_matrix(y, y_pred)

        # Log results for further analysis
        print(f"Metrics for {model_name} at threshold {threshold}: {metrics}")
        print(f"Confusion Matrix:\n{cm}")

        return metrics, cm

    def plot_confusion_matrix(self, cm: np.ndarray, model_name: str, threshold: float):
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Non-Scam', 'Scam'],
                    yticklabels=['Non-Scam', 'Scam'])
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.title(f'Confusion Matrix: {model_name} (Threshold={threshold:.3f})')
        plt.tight_layout()
        plt.savefig(f'{model_name}_confusion_matrix_threshold_{threshold:.3f}.png')
        plt.close()

    def find_optimal_threshold(self, model_name: str, thresholds=np.arange(0.001, 0.99, 0.01)) -> Tuple[float, dict]:
        best_f1 = 0
        best_threshold = 0
        best_metrics = None
        
        for threshold in thresholds:
            metrics, _ = self.evaluate_threshold(model_name, threshold)
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                best_threshold = threshold
                best_metrics = metrics
        
        return best_threshold, best_metrics

    def evaluate_all_models(self, thresholds=None):
        if thresholds is None:
            thresholds = np.arange(0.1, 0.9, 0.1)
        
        results = []
        
        for model_name in self.merged_data.keys():
            print(f"\nEvaluating {model_name}:")
            
            opt_threshold, opt_metrics = self.find_optimal_threshold(model_name)
            print(f"\nOptimal threshold: {opt_threshold:.4f}")
            print("Metrics at optimal threshold:")
            for metric, value in opt_metrics.items():
                print(f"{metric}: {value:.4f}")

            for threshold in thresholds:
                metrics, cm = self.evaluate_threshold(model_name, threshold)
                self.plot_confusion_matrix(cm, model_name, threshold)
                
                results.append({
                    'model': model_name,
                    'threshold': threshold,
                    **metrics
                })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv('412ammodel_train_evaluation_results.csv', index=False)
        return results_df

# Example usage
if __name__ == "__main__":
    ground_truth_path = "ground_truth_labels.csv"
    model_files = {
        'BERT': 'bert_airdrop_sentiment_results.csv',
        'Custom Dict': 'custom_dictionary_airdrop_sentiment_results.csv',
        'RoBERTa': 'roberta_airdrop_sentiment_combined_results.csv',
        'TextBlob': 'textblob_airdrop_sentiment_results.csv',
        'VADER': 'vader_airdrop_sentiment_results_1.csv'
    }
    
    evaluator = ModelEvaluator(ground_truth_path, model_files)
    results_df = evaluator.evaluate_all_models()
    
    print("\nSummary of results across all models and thresholds:")
    print(results_df.sort_values(['model', 'f1'], ascending=[True, False]))
