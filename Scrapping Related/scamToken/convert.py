import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Function to scrape contract name from BscScan token page
def get_contract_name(address):
    url = f"https://bscscan.com/token/{address}#code"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the contract name by locating the correct divs and spans
        contract_name_label = soup.find("div", text="Contract Name:")
        if contract_name_label:
            contract_name_element = contract_name_label.find_next("span")
            if contract_name_element:
                contract_name = contract_name_element.text.strip()
                return contract_name
        return "Unknown Contract Name"
    else:
        return "Error fetching page"

# Load the token addresses from the json file
with open('tokens.json', 'r') as file:
    data = json.load(file)

token_addresses = data.get('tokens', [])

# Fetch contract names for each address
token_data = []
for i, address in enumerate(token_addresses):
    print(f"Fetching contract name for: {address}")
    contract_name = get_contract_name(address)
    token_data.append({'Address': address, 'Contract Name': contract_name})

    # Sleep for a while to avoid overwhelming the server
    time.sleep(1)

# Create a pandas DataFrame
df = pd.DataFrame(token_data)

# Save the DataFrame to an Excel file
output_path = 'contract_names.xlsx'
df.to_excel(output_path, index=False)

print(f'Contract names saved to {output_path}')

