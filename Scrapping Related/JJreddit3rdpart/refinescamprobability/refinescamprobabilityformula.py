#script created to refine the is_scam column to update the formula to become the same threshold

import pandas as pd

# Load the existing sentiment analysis results
input_file = 'roberta_time_decay_weighted_sentiment_results.csv'  # Update this to the correct file path for your saved CSV
df = pd.read_csv(input_file)

# Check that the 'scam_probability' column exists
if 'scam_probability' in df.columns:
    # Update the 'is_scam' column based on the new threshold (0.01)
    df['is_scam'] = df['scam_probability'] > 0.01  # Change the threshold to 0.01
    
    # Save the updated results to a new CSV file
    output_file = 'roberta_time_decay_weighted_sentiment_results_latest.csv'  # You can choose the desired output file name
    df.to_csv(output_file, index=False)
    print(f"Updated results saved to {output_file}")
else:
    print("'scam_probability' column not found in the CSV file.")
