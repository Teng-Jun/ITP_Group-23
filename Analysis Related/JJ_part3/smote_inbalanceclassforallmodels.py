import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, fbeta_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import RobustScaler
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class ImprovedScamDetector:
    def __init__(self, ground_truth_path, model_paths):
        """
        Initialize with paths to ground truth and model prediction files
        
        Args:
            ground_truth_path (str): Path to ground truth labels CSV
            model_paths (dict): Dictionary of model names and their prediction file paths
        """
        self.ground_truth = pd.read_csv(ground_truth_path)
        self.model_data = {}
        
        for model_name, path in model_paths.items():
            try:
                preds = pd.read_csv(path)
                merged = pd.merge(self.ground_truth, preds, 
                                left_on='Token Name', 
                                right_on='airdrop_name', 
                                how='inner')
                self.model_data[model_name] = merged
            except Exception as e:
                print(f"Error loading {model_name} data: {str(e)}")
    
    def create_advanced_features(self, df):
        """Create enhanced features for better classification"""
        features = df.copy()
        
        # Basic probability features
        features['scam_probability'] = pd.to_numeric(features['scam_probability'], errors='coerce')
        features['scam_probability'] = features['scam_probability'].fillna(features['scam_probability'].mean())
        features['scam_probability'] = features['scam_probability'].clip(0, 1)
        
        # Transform features
        features['prob_log'] = np.log1p(features['scam_probability'])
        features['prob_sqrt'] = np.sqrt(features['scam_probability'])
        features['prob_squared'] = features['scam_probability'] ** 2
        features['prob_cube'] = features['scam_probability'] ** 3
        
        # Polynomial features
        features['prob_log_squared'] = features['prob_log'] ** 2
        features['prob_sqrt_squared'] = features['prob_sqrt'] ** 2
        
        # Percentile features
        features['prob_percentile'] = pd.qcut(features['scam_probability'], 
                                            q=10, 
                                            labels=False, 
                                            duplicates='drop')
        
        # Scale features
        scaler = RobustScaler()
        numeric_cols = ['scam_probability', 'prob_log', 'prob_sqrt', 'prob_squared']
        features[numeric_cols] = scaler.fit_transform(features[numeric_cols])
        
        return features
    
    def evaluate_model(self, model_name, n_splits=5):
        """
        Evaluate a specific model with advanced sampling and ensemble methods
        
        Args:
            model_name (str): Name of the model to evaluate
            n_splits (int): Number of cross-validation splits
        """
        print(f"\nEvaluating {model_name}:")
        
        try:
            df = self.model_data[model_name].copy()
            df = self.create_advanced_features(df)
            
            feature_cols = ['scam_probability', 'prob_log', 'prob_sqrt', 'prob_squared',
                          'prob_cube', 'prob_log_squared', 'prob_sqrt_squared',
                          'prob_percentile']
            
            X = df[feature_cols].values
            y = df['Is Scam'].values
            
            print(f"\nOriginal class distribution: {Counter(y)}")
            
            # Initialize samplers with optimized parameters
            smote = SMOTE(sampling_strategy=0.5, k_neighbors=3, random_state=42)
            adasyn = ADASYN(sampling_strategy=0.5, n_neighbors=3, random_state=42)
            smote_tomek = SMOTETomek(sampling_strategy=0.5, random_state=42)
            
            # Create optimized classifiers
            rf = RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=4,
                class_weight='balanced_subsample',
                random_state=42
            )
            
            gb = GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                subsample=0.8,
                random_state=42
            )
            
            # Create pipelines
            pipelines = {
                'smote_rf': Pipeline([
                    ('sampler', smote),
                    ('classifier', rf)
                ]),
                'adasyn_gb': Pipeline([
                    ('sampler', adasyn),
                    ('classifier', gb)
                ]),
                'smotetomek_rf': Pipeline([
                    ('sampler', smote_tomek),
                    ('classifier', rf)
                ])
            }
            
            skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            results = []
            
            for pipeline_name, pipeline in pipelines.items():
                print(f"\nTesting {pipeline_name}...")
                
                for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
                    X_train, X_val = X[train_idx], X[val_idx]
                    y_train, y_val = y[train_idx], y[val_idx]
                    
                    # Fit pipeline
                    pipeline.fit(X_train, y_train)
                    
                    # Try different thresholds
                    thresholds = np.linspace(0.1, 0.9, 50)
                    for threshold in thresholds:
                        y_pred_proba = pipeline.predict_proba(X_val)[:, 1]
                        y_pred = (y_pred_proba >= threshold).astype(int)
                        
                        metrics = {
                            'pipeline': pipeline_name,
                            'fold': fold,
                            'threshold': threshold,
                            'accuracy': accuracy_score(y_val, y_pred),
                            'precision': precision_score(y_val, y_pred, zero_division=0),
                            'recall': recall_score(y_val, y_pred, zero_division=0),
                            'f1': f1_score(y_val, y_pred, zero_division=0),
                            'f2': fbeta_score(y_val, y_pred, beta=2, zero_division=0)
                        }
                        results.append(metrics)
            
            # Convert results to DataFrame
            results_df = pd.DataFrame(results)
            
            # Print summary statistics
            print("\nMetrics summary (mean ± std):")
            summary = results_df.groupby('pipeline')[
                ['accuracy', 'precision', 'recall', 'f1', 'f2']
            ].agg(['mean', 'std']).round(4)
            print(summary)
            
            # Find best configuration
            best_result = results_df.loc[results_df['f2'].idxmax()]
            print(f"\nBest configuration for {model_name}:")
            print(f"Pipeline: {best_result['pipeline']}")
            print(f"Threshold: {best_result['threshold']:.4f}")
            print(f"Accuracy: {best_result['accuracy']:.4f}")
            print(f"Precision: {best_result['precision']:.4f}")
            print(f"Recall: {best_result['recall']:.4f}")
            print(f"F1 Score: {best_result['f1']:.4f}")
            print(f"F2 Score: {best_result['f2']:.4f}")
            
            return results_df
            
        except Exception as e:
            print(f"Error evaluating {model_name}: {str(e)}")
            return pd.DataFrame()

def main():
    # Define file paths
    ground_truth_path = "ground_truth_labels.csv"
    model_files = {
        'BERT': 'bert_airdrop_sentiment_results.csv',
        'RoBERTa': 'roberta_airdrop_sentiment_combined_results.csv',
        'VADER': 'vader_airdrop_sentiment_results_1.csv',
        'TextBlob': 'textblob_airdrop_sentiment_results.csv',
        'Custom Dict': 'custom_dictionary_airdrop_sentiment_results.csv'
    }
    
    # Initialize detector
    detector = ImprovedScamDetector(ground_truth_path, model_files)
    
    # Evaluate all models
    all_results = {}
    for model_name in model_files.keys():
        results = detector.evaluate_model(model_name)
        all_results[model_name] = results
    
    # Compare models
    print("\nModel Comparison (Best F2 Scores):")
    for model_name, results in all_results.items():
        if not results.empty:
            best_f2 = results['f2'].max()
            print(f"{model_name}: {best_f2:.4f}")

if __name__ == "__main__":
    main()