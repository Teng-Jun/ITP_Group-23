import json
import pandas as pd
from web3 import Web3

def connect_to_node(infura_url):
    web3 = Web3(Web3.HTTPProvider(infura_url))
    if not web3.is_connected():
        raise Exception("Failed to connect to the Ethereum node.")
    return web3

def read_token_addresses(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['token_addresses']

# ABI for ERC20 token standard
erc20_abi = '''
[
    {
        "constant": true,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]
'''

def get_token_name(web3, address):
    try:
        checksum_address = web3.to_checksum_address(address)
        contract = web3.eth.contract(address=checksum_address, abi=erc20_abi)
        return contract.functions.name().call()
    except Exception as e:
        return f"Error: {str(e)}"

def fetch_token_data(web3, token_addresses):
    token_data = []
    for token_address in token_addresses:
        token_name = get_token_name(web3, token_address)
        token_data.append({"Token Address": token_address, "Token Name": token_name})
    return token_data

def save_to_excel(token_data, file_name):
    df = pd.DataFrame(token_data)
    df.to_excel(file_name, index=False)
    print(f"Token data has been saved to {file_name}")

# Main function to combine both tasks
def main():
    # Polygon
    polygon_infura_url = 'https://polygon-mainnet.infura.io/v3/a332db307f6c46aeb94eba87b0b7f890'
    polygon_web3 = connect_to_node(polygon_infura_url)
    polygon_token_addresses = read_token_addresses('token_addresses(matic).json')
    polygon_token_data = fetch_token_data(polygon_web3, polygon_token_addresses)
    save_to_excel(polygon_token_data, 'token_names(matic).xlsx')

    # Ethereum
    ethereum_infura_url = 'https://mainnet.infura.io/v3/a332db307f6c46aeb94eba87b0b7f890'
    ethereum_web3 = connect_to_node(ethereum_infura_url)
    ethereum_token_addresses = read_token_addresses('token_addresses(eth).json')
    ethereum_token_data = fetch_token_data(ethereum_web3, ethereum_token_addresses)
    save_to_excel(ethereum_token_data, 'token_names(eth).xlsx')

if __name__ == "__main__":
    main()
