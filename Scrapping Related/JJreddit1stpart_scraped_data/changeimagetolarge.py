import pandas as pd

# Load your CSV file
csv_file = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit1stpart_scraped_data_csv\coingecko_matched_coins_with_images_final_retry3.csv'
coins_df = pd.read_csv(csv_file)

# Replace 'thumb' with 'large' in image URLs
coins_df['image'] = coins_df['image'].apply(lambda x: x.replace('thumb', 'large') if isinstance(x, str) else x)

# Save the updated CSV
output_file = r'C:\Users\dclit\OneDrive\Documents\GitHub\ITP_Group-23\Scrapping Related\JJreddit1stpart_scraped_data_csv\coingecko_matched_coins_with_images_high_res.csv'
coins_df.to_csv(output_file, index=False)

print(f"Updated coin data with high resolution images saved to '{output_file}'")
