import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the full results dataset
results_df = pd.read_csv('results_sentiment_models_boosted/test_set_boosted_comparison_results.csv')

# Define weights for metrics (you can adjust these weights based on priority)
weights = {
    'Precision': 0.2,
    'Recall': 0.2,
    'F1': 0.4,  # F1 is weighted higher since it's usually a key metric for imbalanced data
    'Accuracy': 0.1,
    'ROC AUC': 0.1
}

# Normalize weights to ensure they sum to 1
total_weight = sum(weights.values())
normalized_weights = {key: value / total_weight for key, value in weights.items()}

# Calculate a weighted score for each row in the dataset
results_df['Weighted Score'] = (
    results_df['Precision'] * normalized_weights['Precision'] +
    results_df['Recall'] * normalized_weights['Recall'] +
    results_df['F1'] * normalized_weights['F1'] +
    results_df['Accuracy'] * normalized_weights['Accuracy'] +
    results_df['ROC AUC'] * normalized_weights['ROC AUC']
)

# Identify the best boosting model for each sentiment model based on the weighted score
best_scores = results_df.loc[results_df.groupby('Sentiment Model')['Weighted Score'].idxmax()]

# Save the best scores for reference
best_scores.to_csv('results_sentiment_models_boosted/best_scores_per_sentiment_model_weighted.csv', index=False)

# Prepare data for plotting
metrics = ['Precision', 'Recall', 'F1', 'Accuracy', 'ROC AUC']
x_positions = np.arange(len(best_scores['Sentiment Model']))
bar_width = 0.15
colors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#ff5a5f']

# Create grouped bar chart for all metrics
plt.figure(figsize=(15, 10))

# Iterate through metrics to create grouped bars
for i, metric in enumerate(metrics):
    plt.bar(
        x_positions + i * bar_width,
        best_scores[metric],
        width=bar_width,
        label=metric,
        alpha=0.8,
        color=colors[i]
    )

# Customize the plot
plt.xlabel('Sentiment Models')
plt.ylabel('Scores')
plt.xticks(
    x_positions + bar_width * (len(metrics) - 1) / 2,
    best_scores['Sentiment Model'],
    rotation=45,
    ha='right'
)
plt.ylim(0, 1)  # All metrics are percentages
plt.legend()

# Annotate each bar with its value
for i, metric in enumerate(metrics):
    for j, value in enumerate(best_scores[metric]):
        plt.text(
            x_positions[j] + i * bar_width,
            value + 0.02,
            f'{value:.2f}',
            ha='center',
            va='bottom',
            fontsize=8,
            rotation=90
        )

# Adjust layout and title placement
plt.title(
    'Model Performance Comparison for Airdrop Scam Detection (Best Configurations)',
    pad=50
)
plt.tight_layout(rect=[0, 0, 1, 0.9])  # Adjust layout to allow more space at the top

# Save the plot
plt.savefig('results_sentiment_models_boosted/model_comparison_best_scores_weighted_combined.png', dpi=300, bbox_inches='tight')
print("Plot saved as 'results_sentiment_models_boosted/model_comparison_best_scores_weighted_combined.png'")

# Show the plot
plt.show()
