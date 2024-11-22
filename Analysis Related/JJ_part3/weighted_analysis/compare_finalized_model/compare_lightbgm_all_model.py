import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create data dictionary specifically for LightGBM models
data = {
    'Model': [
        'LightGBM-VADER', 'LightGBM-BERT', 'LightGBM-Custom',
        'LightGBM-TextBlob', 'LightGBM-Roberta'
    ],
    'Precision': [
        0.78125, 0.9523809523809523, 1.0,
        0.95, 0.975308642
    ],
    'Recall': [
        0.9393939393939394, 0.963303, 0.8947368421052632,
        0.8333333333333334, 0.943181818
    ],
    'F1': [
        0.775, 0.9345794392523364, 0.9444444444444444,
        0.8636363636363636, 0.954022989
    ],
    'Accuracy': [
        0.9544159544159544, 0.9601139601139601, 0.9943019943019943,
        0.9829059829059829, 0.977207977
    ]
}

# Convert to DataFrame for easier plotting
df = pd.DataFrame(data)

# Set up the plot
plt.figure(figsize=(15, 8))

# Create bar positions for each metric
bar_width = 0.2
r1 = np.arange(len(df['Model']))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Plot bars for each metric
bars1 = plt.bar(r1, df['Precision'], width=bar_width, label='Precision', color='#8884d8', alpha=0.8)
bars2 = plt.bar(r2, df['Recall'], width=bar_width, label='Recall', color='#82ca9d', alpha=0.8)
bars3 = plt.bar(r3, df['F1'], width=bar_width, label='F1 Score', color='#ffc658', alpha=0.8)
bars4 = plt.bar(r4, df['Accuracy'], width=bar_width, label='Accuracy', color='#ff7300', alpha=0.8)

# Add value labels on top of each bar
def add_value_labels(bars):
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, f'{yval:.2f}', ha='center', va='bottom', fontsize=10)

add_value_labels(bars1)
add_value_labels(bars2)
add_value_labels(bars3)
add_value_labels(bars4)

# Customize the plot
plt.xlabel('Models')
plt.ylabel('Scores')
plt.title('LightGBM Model Performance Comparison for Airdrop Scam Detection')
plt.xticks([r + bar_width*1.5 for r in range(len(df['Model']))], df['Model'], rotation=45, ha='right')
plt.legend()

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Add grid for better readability
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Set y-axis limits
plt.ylim(0, 1.1)

# Display the plot
plt.show()
