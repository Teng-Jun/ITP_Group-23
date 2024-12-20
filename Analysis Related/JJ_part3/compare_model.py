import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import precision_recall_curve, roc_curve, auc
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Tuple
import os

class ModelEvaluator:
    def __init__(self, ground_truth_path: str, predictions_paths: Dict[str, str]):
        self.ground_truth = pd.read_csv(ground_truth_path)
        self.predictions = {}
        self.merged_data = {}

        for model_name, path in predictions_paths.items():
            preds = pd.read_csv(path)
            merged = pd.merge(self.ground_truth, preds, 
                            left_on='Token Name', 
                            right_on='airdrop_name', 
                            how='inner')
            self.merged_data[model_name] = merged

    def evaluate_threshold(self, model_name: str, threshold: float) -> Tuple[dict, np.ndarray]:
        df = self.merged_data[model_name]
        y_pred = (df['scam_probability'] > threshold).astype(int)
        y_true = df['Is Scam'].astype(int)

        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1': f1_score(y_true, y_pred, zero_division=0)
        }
        
        cm = confusion_matrix(y_true, y_pred)
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
        plt.savefig(f'{model_name}_confusion_matrix_threshold_{threshold:.3f}.png')  # Save plot as PNG
        plt.close()  # Close the figure

    def plot_pr_curve(self, model_name: str):
        df = self.merged_data[model_name]
        y_true = df['Is Scam'].astype(int)
        y_scores = df['scam_probability']

        precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
        
        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, label=f'{model_name} (AUC={auc(recall, precision):.3f})')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title(f'Precision-Recall Curve: {model_name}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{model_name}_precision_recall_curve.png')  # Save PR curve
        plt.close()  # Close the figure

    def plot_roc_curve(self, model_name: str):
        df = self.merged_data[model_name]
        y_true = df['Is Scam'].astype(int)
        y_scores = df['scam_probability']

        fpr, tpr, _ = roc_curve(y_true, y_scores)
        roc_auc = auc(fpr, tpr)

        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'{model_name} (AUC={roc_auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve: {model_name}')
        plt.legend()
        plt.grid(True)
        plt.savefig(f'{model_name}_roc_curve.png')  # Save ROC curve
        plt.close()  # Close the figure

    def find_optimal_threshold(self, model_name: str, 
                             thresholds=np.arange(0.001, 0.01, 0.0005)) -> Tuple[float, dict]:
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
            thresholds = [0.0050, 0.0035, 0.0095, 0.0030, 0.0010]
        
        results = []
        
        for model_name in self.merged_data.keys():
            print(f"\nEvaluating {model_name}:")
            
            opt_threshold, opt_metrics = self.find_optimal_threshold(model_name)
            print(f"\nOptimal threshold: {opt_threshold:.4f}")
            print("Metrics at optimal threshold:")
            for metric, value in opt_metrics.items():
                print(f"{metric}: {value:.4f}")
            
            self.plot_pr_curve(model_name)
            self.plot_roc_curve(model_name)
            
            for threshold in thresholds:
                metrics, cm = self.evaluate_threshold(model_name, threshold)
                self.plot_confusion_matrix(cm, model_name, threshold)
                
                results.append({
                    'model': model_name,
                    'threshold': threshold,
                    **metrics
                })
        
        results_df = pd.DataFrame(results)
        results_df.to_csv('model_evaluation_results.csv', index=False)  # Save results to CSV
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
