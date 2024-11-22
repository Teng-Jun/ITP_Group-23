import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create data dictionary for all models
data = {
    'Model': [
        # VADER
        'XGBoost-VADER', 'LightGBM-VADER', 'RandomForest-VADER',
        # BERT
        'XGBoost-BERT', 'LightGBM-BERT', 'RandomForest-BERT',
        # Custom
        'XGBoost-Custom', 'LightGBM-Custom', 'RandomForest-Custom',
        # TextBlob
        'XGBoost-TextBlob', 'LightGBM-TextBlob', 'RandomForest-TextBlob',
        # Roberta
        'XGBoost-Roberta', 'LightGBM-Roberta', 'RandomForest-Roberta'
    ],
    'Precision': [
        # VADER
        0.5172413793103449, 0.78125, 0.34444444444444444,
        # BERT
        0.9339622641509434, 0.9523809523809523, 0.8648648648648649,
        # Custom
        0.5135135135135135, 1.0, 0.4444444444444444,
        # TextBlob
        0.6052631578947368, 0.95, 0.9,
        #Roberta
        0.885416667, 0.975308642, 0.875

    ],
    'Recall': [
        # VADER
        0.8823529411764706, 0.9393939393939394, 1.0,
        # BERT
        0.9541284403669725, 0.963303, 0.908257,
        # Custom
        1.0, 0.8947368421052632, 0.9473684210526315,
        # TextBlob
        0.9583333333333334, 0.8333333333333334, 0.8333333333333334,
        #Roberta
        0.965909091,0.943181818, 0.942528736

    ],
    'F1': [
        # VADER
        0.6521739130434783, 0.775, 0.5040650406504065,
        # BERT
        0.9209302325581395, 0.9345794392523364, 0.8727272727272727,
        # Custom
        0.6785714285714286, 0.9444444444444444, 0.5217391304347826,
        # TextBlob
        0.7419354838709677, 0.8636363636363636, 0.6486486486486487,
        #Roberta
        0.923913043, 0.954022989, 0.839779006

    ],
    'Accuracy': [
        # VADER
        0.9088319088319088, 0.9544159544159544, 0.8257142857142857,
        # BERT
        0.9514285714285714, 0.9601139601139601, 0.9202279202279202,
        # Custom
        0.9487179487179487, 0.9943019943019943, 0.9373219373219374,
        # TextBlob
        0.9544159544159544, 0.9829059829059829, 0.9628571428571429,
        #Roberta
        0.96011396, 0.977207977, 0.922857143

    ]
}

# Convert to DataFrame for easier plotting
df = pd.DataFrame(data)

# Set up the plot style
#plt.style.use('seaborn')
plt.figure(figsize=(15, 10))

# Create bar positions
bar_width = 0.2
r1 = np.arange(len(df['Model']))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Create bars
plt.bar(r1, df['Precision'], width=bar_width, label='Precision', color='#8884d8', alpha=0.8)
plt.bar(r2, df['Recall'], width=bar_width, label='Recall', color='#82ca9d', alpha=0.8)
plt.bar(r3, df['F1'], width=bar_width, label='F1 Score', color='#ffc658', alpha=0.8)
plt.bar(r4, df['Accuracy'], width=bar_width, label='Accuracy', color='#ff7300', alpha=0.8)

# Customize the plot
plt.xlabel('Models')
plt.ylabel('Scores')
plt.title('Model Performance Comparison for Airdrop Scam Detection')
plt.xticks([r + bar_width*1.5 for r in range(len(df['Model']))], df['Model'], rotation=45, ha='right')
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Add grid for better readability
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Set y-axis limits
plt.ylim(0, 1.1)

# Save the plot
plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
print("Plot has been saved as 'model_comparison.png'")

# Optional: Create a more detailed version with annotated values
plt.figure(figsize=(15, 10))

# Create the same plot structure but add value annotations
plt.bar(r1, df['Precision'], width=bar_width, label='Precision', color='#8884d8', alpha=0.8)
plt.bar(r2, df['Recall'], width=bar_width, label='Recall', color='#82ca9d', alpha=0.8)
plt.bar(r3, df['F1'], width=bar_width, label='F1 Score', color='#ffc658', alpha=0.8)
plt.bar(r4, df['Accuracy'], width=bar_width, label='Accuracy', color='#ff7300', alpha=0.8)

# Add value annotations
def add_value_labels(positions, values):
    for pos, value in zip(positions, values):
        plt.text(pos, value, f'{value:.2f}', ha='center', va='bottom', rotation=90, fontsize=8)

add_value_labels(r1, df['Precision'])
add_value_labels(r2, df['Recall'])
add_value_labels(r3, df['F1'])
add_value_labels(r4, df['Accuracy'])

# Customize the plot
plt.xlabel('Models')
plt.ylabel('Scores')
plt.title('Model Performance Comparison for Airdrop Scam Detection (with values)')
plt.xticks([r + bar_width*1.5 for r in range(len(df['Model']))], df['Model'], rotation=45, ha='right')
plt.legend()
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, 1.1)
plt.tight_layout()

# Save the detailed version
plt.savefig('model_comparison_with_values.png', dpi=300, bbox_inches='tight')
print("Detailed plot has been saved as 'model_comparison_with_values.png'")