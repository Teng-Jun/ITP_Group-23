import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple
from collections import Counter

class EnhancedModelValidator:
    def __init__(self, ground_truth_path: str, predictions_paths: Dict[str, str], 
                 test_size=0.2, random_state=42):
        self.random_state = random_state
        self.test_size = test_size
        self.ground_truth = pd.read_csv(ground_truth_path)
        self.predictions = {}
        self.merged_data = {}
        
        # Load and preprocess data
        for model_name, path in predictions_paths.items():
            preds = pd.read_csv(path)
            merged = pd.merge(self.ground_truth, preds, 
                            left_on='Token Name', 
                            right_on='airdrop_name', 
                            how='inner')
            
            # Normalize probabilities
            scaler = StandardScaler()
            merged['scam_probability'] = scaler.fit_transform(
                merged['scam_probability'].values.reshape(-1, 1))
            merged['scam_probability'] = self.sigmoid(merged['scam_probability'])
            
            self.merged_data[model_name] = merged
    
    def sigmoid(self, x):
        """Apply sigmoid transformation to normalize probabilities"""
        return 1 / (1 + np.exp(-x))

    def prepare_balanced_datasets(self, df: pd.DataFrame) -> Tuple:
        """Prepare datasets with improved balancing strategy"""
        X = df[['scam_probability']].values
        y = df['Is Scam'].values
        
        # First split to preserve test set distribution
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, stratify=y, 
            random_state=self.random_state
        )
        
        print("Initial class distribution:", Counter(y_train))
        
        # Create balanced training set
        sampling_pipeline = Pipeline([
            ('undersample', RandomUnderSampler(sampling_strategy=0.5)),
            ('smote', SMOTE(sampling_strategy=1.0, k_neighbors=5))
        ])
        
        X_train_balanced, y_train_balanced = sampling_pipeline.fit_resample(X_train, y_train)
        print("Balanced class distribution:", Counter(y_train_balanced))
        
        return X_train_balanced, X_test, y_train_balanced, y_test

    def find_optimal_threshold(self, X: np.ndarray, y: np.ndarray) -> float:
        """Find optimal threshold using grid search with F1 optimization"""
        thresholds = np.linspace(0.2, 0.8, 100)
        best_f1 = 0
        best_threshold = 0.5
        
        for threshold in thresholds:
            y_pred = (X.ravel() > threshold).astype(int)
            f1 = f1_score(y, y_pred)
            
            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold
        
        return best_threshold

    def evaluate_model(self, model_name: str) -> Dict:
        """Evaluate model with enhanced metrics"""
        df = self.merged_data[model_name]
        X_train, X_test, y_train, y_test = self.prepare_balanced_datasets(df)
        
        # Find optimal threshold on training data
        threshold = self.find_optimal_threshold(X_train, y_train)
        
        # Generate predictions
        y_train_pred = (X_train.ravel() > threshold).astype(int)
        y_test_pred = (X_test.ravel() > threshold).astype(int)
        
        # Calculate metrics
        train_metrics = {
            'accuracy': accuracy_score(y_train, y_train_pred),
            'precision': precision_score(y_train, y_train_pred),
            'recall': recall_score(y_train, y_train_pred),
            'f1': f1_score(y_train, y_train_pred)
        }
        
        test_metrics = {
            'accuracy': accuracy_score(y_test, y_test_pred),
            'precision': precision_score(y_test, y_test_pred),
            'recall': recall_score(y_test, y_test_pred),
            'f1': f1_score(y_test, y_test_pred)
        }
        
        # Plot confusion matrices
        self.plot_confusion_matrices(y_train, y_train_pred, 
                                   y_test, y_test_pred, model_name)
        
        return {
            'threshold': threshold,
            'train_metrics': train_metrics,
            'test_metrics': test_metrics
        }

    def plot_confusion_matrices(self, y_train, y_train_pred, 
                              y_test, y_test_pred, model_name):
        """Plot confusion matrices for both training and test sets"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Training confusion matrix
        cm_train = pd.crosstab(y_train, y_train_pred, 
                              normalize='index') * 100
        sns.heatmap(cm_train, annot=True, fmt='.1f', cmap='Blues', ax=ax1)
        ax1.set_title(f'{model_name} - Training Confusion Matrix (%)')
        
        # Test confusion matrix
        cm_test = pd.crosstab(y_test, y_test_pred, 
                             normalize='index') * 100
        sns.heatmap(cm_test, annot=True, fmt='.1f', cmap='Blues', ax=ax2)
        ax2.set_title(f'{model_name} - Test Confusion Matrix (%)')
        
        plt.tight_layout()
        plt.show()

    def evaluate_all_models(self):
        """Evaluate all models and generate comprehensive report"""
        results = {}
        
        for model_name in self.merged_data.keys():
            print(f"\nEvaluating {model_name}:")
            model_results = self.evaluate_model(model_name)
            results[model_name] = model_results
            
            print(f"\nOptimal threshold: {model_results['threshold']:.4f}")
            print("\nTraining Metrics:")
            for metric, value in model_results['train_metrics'].items():
                print(f"{metric}: {value:.4f}")
            print("\nTest Metrics:")
            for metric, value in model_results['test_metrics'].items():
                print(f"{metric}: {value:.4f}")
        
        return results

# Usage
if __name__ == "__main__":
    ground_truth_path = "ground_truth_labels.csv"
    model_files = {
        'BERT': 'bert_airdrop_sentiment_results.csv',
        'Custom Dict': 'custom_dictionary_airdrop_sentiment_results.csv',
        'RoBERTa': 'roberta_airdrop_sentiment_combined_results.csv',
        'TextBlob': 'textblob_airdrop_sentiment_results.csv',
        'VADER': 'vader_airdrop_sentiment_results_1.csv'
    }
    
    validator = EnhancedModelValidator(ground_truth_path, model_files)
    results = validator.evaluate_all_models()