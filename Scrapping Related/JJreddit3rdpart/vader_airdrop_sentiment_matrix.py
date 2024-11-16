import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
import os
import warnings
warnings.filterwarnings('ignore')

class ScamDetectionSystem:
    def __init__(self, data_path):
        self.DATA_PATH = data_path
        self.feature_columns = [
            'sentiment_intensity',
            'engagement_score',
            'comment_quality',
            'activity_rate',
            'neg_pos_ratio',
            'negative_percentage',
            'positive_percentage',
            'average_comment_length',
            'comment_count',
            'total_upvotes',
            'sentiment_volatility',
            'sentiment_trend',
            'engagement_growth',
            'comment_depth',
            'weighted_sentiment',
            'sentiment_engagement_ratio',
            'controversy_score'
        ]

    def load_data(self):
        """Load and merge the required datasets"""
        sentiment_results_df = pd.read_csv(os.path.join(self.DATA_PATH, 'vader_airdrop_sentiment_results_ver2.csv'))
        ground_truth_df = pd.read_csv(os.path.join(self.DATA_PATH, 'ground_truth_labels.csv'))
        
        # Calculate features
        features_df = self.calculate_features(sentiment_results_df)
        
        # Merge with ground truth
        merged_df = pd.merge(
            features_df,
            ground_truth_df[['Token Name', 'Is Scam']],
            left_on='airdrop_name',
            right_on='Token Name',
            how='inner'
        )
        
        return merged_df

    def calculate_features(self, df):
        """Calculate all features for the model"""
        features_df = df.copy()
        features_df = features_df.fillna(0)
        
        # Calculate total if not present
        if 'total' not in features_df.columns:
            features_df['total'] = features_df['positive'] + features_df['negative'] + features_df['neutral']
        
        # Basic features
        features_df['sentiment_intensity'] = np.where(
            features_df['total'] > 0,
            (features_df['negative'] - features_df['positive']) / features_df['total'],
            0
        )
        
        features_df['engagement_score'] = np.where(
            features_df['comment_count'] > 0,
            np.log1p(features_df['total_upvotes']) / np.log1p(features_df['comment_count']),
            0
        )
        
        features_df['comment_quality'] = np.where(
            features_df['comment_count'] > 0,
            features_df['total_words'] / features_df['comment_count'],
            0
        )
        
        features_df['activity_rate'] = np.where(
            features_df['post_age_days'] > 0,
            features_df['comment_count'] / features_df['post_age_days'],
            0
        )
        
        features_df['neg_pos_ratio'] = np.where(
            features_df['positive'] > 0,
            features_df['negative'] / features_df['positive'],
            features_df['negative']
        )
        
        features_df['negative_percentage'] = np.where(
            features_df['total'] > 0,
            (features_df['negative'] / features_df['total']) * 100,
            0
        )
        
        features_df['positive_percentage'] = np.where(
            features_df['total'] > 0,
            (features_df['positive'] / features_df['total']) * 100,
            0
        )
        
        # Enhanced features using available columns
        features_df['average_comment_length'] = features_df['total_words'] / (features_df['comment_count'] + 1)
        
        # Calculate sentiment volatility using positive/negative ratio
        features_df['sentiment_ratio'] = features_df['positive'] / (features_df['negative'] + 1)
        features_df['sentiment_volatility'] = features_df.groupby('airdrop_name')['sentiment_ratio'].transform('std').fillna(0)
        
        # Calculate sentiment trend using the ratio
        features_df['sentiment_trend'] = features_df.groupby('airdrop_name')['sentiment_ratio'].transform(lambda x: x.diff().fillna(0))
        
        # Engagement features
        features_df['engagement_growth'] = features_df.groupby('airdrop_name')['total_upvotes'].transform(lambda x: x.pct_change().fillna(0))
        features_df['comment_depth'] = features_df['total_words'] / (features_df['comment_count'] + 1)
        
        # Time-based features
        features_df['recent_activity_weight'] = np.exp(-features_df['post_age_days'] / 30)
        features_df['weighted_sentiment'] = (features_df['positive'] - features_df['negative']) * features_df['recent_activity_weight']
        
        # Interaction features
        features_df['sentiment_engagement_ratio'] = (features_df['positive'] - features_df['negative']) * features_df['total_upvotes']
        features_df['controversy_score'] = abs(features_df['positive'] - features_df['negative']) * features_df['total']
        
        return features_df

    def create_model(self):
        """Create the model pipeline with SMOTE and RandomForest"""
        param_dist = {
            'rf__n_estimators': [200, 300, 400],
            'rf__max_depth': [6, 8, 10, None],
            'rf__min_samples_split': [2, 5, 10],
            'rf__min_samples_leaf': [1, 2, 4],
            'rf__class_weight': ['balanced', 'balanced_subsample']
        }
        
        pipeline = Pipeline([
            ('smote', SMOTE(random_state=42, sampling_strategy=0.5)),
            ('rf', RandomForestClassifier(random_state=42))
        ])
        
        random_search = RandomizedSearchCV(
            pipeline,
            param_distributions=param_dist,
            n_iter=20,
            cv=5,
            scoring='f1',
            random_state=42,
            n_jobs=-1
        )
        
        return random_search

    def train_and_evaluate(self):
        """Main function to train and evaluate the model"""
        # Load and prepare data
        print("Loading and preparing data...")
        merged_df = self.load_data()
        
        # Prepare features and target
        X = merged_df[self.feature_columns].values
        y = merged_df['Is Scam'].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Initialize variables for cross-validation
        n_splits = 5
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        cv_results = []
        all_predictions = np.zeros(len(y))
        all_probabilities = np.zeros(len(y))
        
        print("\nTraining and evaluating model...")
        # Perform cross-validation
        for fold, (train_idx, val_idx) in enumerate(skf.split(X_scaled, y), 1):
            print(f"\nProcessing fold {fold}/{n_splits}")
            
            # Split data
            X_train, X_val = X_scaled[train_idx], X_scaled[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            # Create and train model
            model = self.create_model()
            model.fit(X_train, y_train)
            
            # Get predictions
            val_pred = model.predict(X_val)
            val_proba = model.predict_proba(X_val)[:, 1]
            
            # Store predictions and probabilities
            all_predictions[val_idx] = val_pred
            all_probabilities[val_idx] = val_proba
            
            # Calculate metrics
            fold_precision = precision_score(y_val, val_pred, zero_division=0)
            fold_recall = recall_score(y_val, val_pred, zero_division=0)
            fold_f1 = f1_score(y_val, val_pred, zero_division=0)
            
            cv_results.append({
                'fold': fold,
                'precision': fold_precision,
                'recall': fold_recall,
                'f1': fold_f1,
                'best_params': model.best_params_
            })
            
            print(f"Fold {fold} Results:")
            print(f"Precision: {fold_precision:.4f}")
            print(f"Recall: {fold_recall:.4f}")
            print(f"F1 Score: {fold_f1:.4f}")
        
        # Calculate final metrics
        final_precision = precision_score(y, all_predictions, zero_division=0)
        final_recall = recall_score(y, all_predictions, zero_division=0)
        final_f1 = f1_score(y, all_predictions, zero_division=0)
        final_accuracy = accuracy_score(y, all_predictions)
        
        # Store results
        merged_df['predicted_scam'] = all_predictions
        merged_df['scam_probability'] = all_probabilities
        
        return {
            'cv_results': cv_results,
            'final_metrics': {
                'precision': final_precision,
                'recall': final_recall,
                'f1': final_f1,
                'accuracy': final_accuracy
            },
            'confusion_matrix': confusion_matrix(y, all_predictions),
            'predictions_df': merged_df
        }

    def save_results(self, results, output_file='scam_detection_results_detailed.csv'):
        """Save the detailed results to a CSV file"""
        results['predictions_df'].to_csv(output_file, index=False)
        print(f"\nDetailed results saved to {output_file}")

def main():
    # Set your data path
    DATA_PATH = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit3rdpart'
    
    # Initialize the system
    detector = ScamDetectionSystem(DATA_PATH)
    
    # Train and evaluate
    results = detector.train_and_evaluate()
    
    # Print final results
    print("\nFinal Metrics:")
    print(f"Precision: {results['final_metrics']['precision']:.4f}")
    print(f"Recall: {results['final_metrics']['recall']:.4f}")
    print(f"F1 Score: {results['final_metrics']['f1']:.4f}")
    print(f"Accuracy: {results['final_metrics']['accuracy']:.4f}")
    
    print("\nConfusion Matrix:")
    print(results['confusion_matrix'])
    
    # Save results
    detector.save_results(results)
    
    # Print analysis of predicted scams
    print("\nAnalysis of Predicted Scams:")
    predicted_scams = results['predictions_df'][results['predictions_df']['predicted_scam'] == 1]
    predicted_scams = predicted_scams.sort_values('scam_probability', ascending=False)
    print(predicted_scams[['airdrop_name', 'scam_probability', 'predicted_scam', 'Is Scam']].head(10))

if __name__ == "__main__":
    main()