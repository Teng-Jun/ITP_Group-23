import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Load the data
file_path = 'testing_data_with_predictions_rf_itp2.csv'
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
data.head()

# Generate confusion matrix
cm = confusion_matrix(data['is_scam'], data['Prediction'])

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
plt.title('Confusion Matrix of Airdrop Predictions')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks([0.5, 1.5], ['Not Scam', 'Scam'])
plt.yticks([0.5, 1.5], ['Not Scam', 'Scam'], rotation=0)
plt.show()
