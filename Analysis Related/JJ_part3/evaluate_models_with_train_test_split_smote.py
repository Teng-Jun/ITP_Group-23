import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, roc_auc_score, average_precision_score,
    classification_report
)
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.combine import SMOTETomek
from imblearn.pipeline import Pipeline
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

warnings.filterwarnings('ignore')

class EnhancedModelEvaluator:
    def __init__(self, ground_truth_path: str, predictions_paths: Dict[str, str]):
        self.ground_truth = pd.read_csv(ground_truth_path)
        self.merged_data = {}
        self.cv_results = {}
        
        # Load and merge data
        for model_name, path in predictions_paths.items():
            preds = pd.read_csv(path)
            merged = pd.merge(self.ground_truth, preds, 
                            left_on='Token Name', 
                            right_on='airdrop_name', 
                            how='inner')
            self.merged_data[model_name] = merged

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced feature engineering with more sophisticated transformations."""
        features = df.copy()
        
        # Ensure numeric probabilities
        features['scam_probability'] = pd.to_numeric(features['scam_probability'], errors='coerce')
        features['scam_probability'] = features['scam_probability'].fillna(features['scam_probability'].mean())
        features['scam_probability'] = features['scam_probability'].clip(0, 1)

        # Advanced feature engineering
        features['prob_log'] = np.log1p(features['scam_probability'])
        features['prob_sqrt'] = np.sqrt(features['scam_probability'])
        features['prob_squared'] = features['scam_probability'] ** 2
        features['prob_cube'] = features['scam_probability'] ** 3
        features['prob_exp'] = np.exp(features['scam_probability']) - 1
        
        # Interaction features
        features['prob_log_squared'] = features['prob_log'] ** 2
        features['prob_sqrt_cube'] = features['prob_sqrt'] ** 3
        
        return features

    def get_model_configurations(self) -> Dict:
        return {
            'rf_balanced': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=4,
                min_samples_leaf=2,
                max_features='sqrt',
                class_weight='balanced',  # Adjust class weight
                random_state=42
            ),
            'gb_balanced': GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                min_samples_split=4,
                min_samples_leaf=2,
                subsample=0.8,
                random_state=42
            )
        }

    def create_resampling_pipelines(self) -> Dict:
        """Create multiple resampling strategies."""
        return {
            'smote': SMOTE(random_state=42, k_neighbors=3),
            'adasyn': ADASYN(random_state=42, n_neighbors=3),
            'smote_tomek': SMOTETomek(random_state=42)
        }

    def evaluate_with_cross_validation(self, model_name: str, n_splits: int = 5) -> Tuple[Dict, List]:
        """Enhanced cross-validation with multiple models and resampling strategies."""
        df = self.merged_data[model_name]
        df = self.create_features(df)

        X = df[[col for col in df.columns if 'prob' in col]]
        y = df['Is Scam'].astype(int)

        print(f"\nClass distribution for {model_name}:")
        print(y.value_counts())
        print(f"Class imbalance ratio: 1:{y.value_counts()[0]/y.value_counts()[1]:.1f}")

        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        
        models = self.get_model_configurations()
        resamplers = self.create_resampling_pipelines()
        
        best_pipeline = None
        best_f1 = -1
        all_fold_results = []

        for model_type, model in models.items():
            for resampler_name, resampler in resamplers.items():
                print(f"\nEvaluating {model_type} with {resampler_name}")
                
                pipeline = Pipeline([
                    ('scaler', StandardScaler()),
                    ('resampler', resampler),
                    ('classifier', model)
                ])

                fold_metrics = []
                for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), 1):
                    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

                    pipeline.fit(X_train, y_train)
                    y_pred = pipeline.predict(X_test)
                    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]

                    fold_result = {
                        'model': model_type,
                        'resampler': resampler_name,
                        'fold': fold,
                        'accuracy': accuracy_score(y_test, y_pred),
                        'precision': precision_score(y_test, y_pred, zero_division=0),
                        'recall': recall_score(y_test, y_pred, zero_division=0),
                        'f1': f1_score(y_test, y_pred, zero_division=0),
                        'auc_roc': roc_auc_score(y_test, y_pred_proba),
                        'avg_precision': average_precision_score(y_test, y_pred_proba)
                    }
                    
                    fold_metrics.append(fold_result)
                    all_fold_results.append(fold_result)

                    print(f"\nFold {fold} Results:")
                    print(classification_report(y_test, y_pred))

                # Check if this is the best performing pipeline
                avg_f1 = np.mean([m['f1'] for m in fold_metrics])
                if avg_f1 > best_f1:
                    best_f1 = avg_f1
                    best_pipeline = pipeline

        # Calculate and store average metrics
        metrics_df = pd.DataFrame(all_fold_results)
        avg_metrics = metrics_df.groupby(['model', 'resampler']).mean().round(4)
        print("\nAverage metrics across all configurations:")
        print(avg_metrics)

        return avg_metrics.to_dict(), best_pipeline

    def plot_evaluation_results(self, model_name: str, metrics: Dict):
        """Create detailed visualization of model performance."""
        plt.figure(figsize=(15, 10))
        
        metrics_df = pd.DataFrame(metrics).reset_index()
        metrics_df = metrics_df.melt(id_vars=['model', 'resampler'], 
                                   var_name='metric', 
                                   value_name='score')

        sns.boxplot(data=metrics_df, x='metric', y='score', hue='model')
        plt.title(f'Performance Metrics Distribution - {model_name}')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{model_name}_performance_metrics.png')
        plt.close()

    def evaluate_all_models(self):
        """Evaluate all models with enhanced reporting."""
        all_results = []
        best_pipelines = {}
        
        for model_name in self.merged_data.keys():
            print(f"\nEvaluating {model_name}...")
            metrics, best_pipeline = self.evaluate_with_cross_validation(model_name)
            
            # Store results and best pipeline
            all_results.append({
                'model': model_name,
                'metrics': metrics
            })
            best_pipelines[model_name] = best_pipeline
            
            # Plot results
            self.plot_evaluation_results(model_name, metrics)

        # Create comprehensive report
        report_df = pd.DataFrame([{
            'model': result['model'],
            **{f"{metric}_{model_type}_{resampler}": value
               for (model_type, resampler), metrics in result['metrics'].items()
               for metric, value in metrics.items()}
        } for result in all_results])

        report_df.to_csv('enhanced_model_evaluation_results.csv', index=False)
        print("\nFinal Results Summary:")
        print(report_df.to_string())
        
        return report_df, best_pipelines

if __name__ == "__main__":
    ground_truth_path = "ground_truth_labels.csv"
    model_files = {
        'BERT': 'bert_airdrop_sentiment_results.csv',
        'Custom Dict': 'custom_dictionary_airdrop_sentiment_results.csv',
        'RoBERTa': 'roberta_airdrop_sentiment_combined_results.csv',
        'TextBlob': 'textblob_airdrop_sentiment_results.csv',
        'VADER': 'vader_airdrop_sentiment_results_1.csv'
    }
    
    evaluator = EnhancedModelEvaluator(ground_truth_path, model_files)
    results, best_pipelines = evaluator.evaluate_all_models()