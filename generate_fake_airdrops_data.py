import pandas as pd
import numpy as np

# Set the number of fake airdrop samples you want to generate
num_fake_samples = 153

# Function to generate random titles for fake airdrops
def generate_title(index):
    return f"FakeAirdrop{index+1}"

# Define the characteristics based on the guidelines for fake airdrops
data = {
    'Title': [generate_title(i) for i in range(num_fake_samples)],                    # Generate fake titles
    'Num_Of_Prev_Drops': np.random.choice([0, 1], size=num_fake_samples, p=[0.8, 0.2]),  # 80% with no previous drops
    'Whitepaper': np.random.choice([0, 1], size=num_fake_samples, p=[0.9, 0.1]),        # 90% with no whitepaper
    'Requirement_Count': np.random.randint(0, 2, size=num_fake_samples),               # Random 0 or 1 requirements
    'Guide_Length': np.random.randint(0, 5, size=num_fake_samples),                    # Small guide length between 0 and 4
    'Social_Media_Count': np.random.randint(0, 3, size=num_fake_samples),              # 0 to 2 social media links
    'Temp': np.random.randint(-10, 5, size=num_fake_samples)                            # Reputation indicator between 1 and 50
}

# Create a DataFrame to hold the fake airdrop data
fake_airdrops_df = pd.DataFrame(data)

# Save the generated data to a CSV file
output_file_path = 'more_training_airdrops_data.csv'
fake_airdrops_df.to_csv(output_file_path, index=False)

print(f"Fake airdrops data with generic titles generated and saved to {output_file_path}")
