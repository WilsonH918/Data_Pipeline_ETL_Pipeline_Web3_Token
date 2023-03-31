from datetime import datetime
import json
import requests

def run_extract(input_contract_address):
    # Set API key and ERC-20 token address
    api_key = 'MY API KEY'
    contract_address = input_contract_address

    api_endpoint = 'https://api.etherscan.io/api'
    api_params = {
        'module': 'account',
        'action': 'tokentx',
        'contractaddress': contract_address,
        'sort': 'desc',  # Sort transactions in descending order (most recent first)
        'offset': 50,  # Skip the first transaction (this is optional)
        'page': 1,  # Get transactions from the first page
        'apikey': api_key
    }

    transactions = []  # Initialize an empty list to store transaction data

    # Paginate through the transaction results until we have xx transactions
    response = requests.get(api_endpoint, params=api_params)
    data = json.loads(response.text)['result']
    transactions.extend(data)  # Add the transactions from this page to our list
    api_params['page'] += 1  # Move to the next page of transactions

    # print(transactions)

    # Convert value to actual value
    for d in transactions:
        d['value'] = float(d['value'])/10**6

    # Sort data by timestamp in descending order
    sorted_data = sorted(transactions, key=lambda k: k['timeStamp'], reverse=True)

    # Convert timestamp in sorted_data to yyyy/mm/dd HH:MM:SS format
    for d in sorted_data:
        d['dateTime'] = datetime.fromtimestamp(int(d['timeStamp'])).strftime('%Y-%m-%dT%H:%M:%S')

    return sorted_data



def run_transform(sorted_data):

    # Transform data as necessary
    transformed_data = []
    for d in sorted_data:
        if float(d['value']) > 1000:
            d['amount_flag'] = 'Y'
        else:
            d['amount_flag'] = 'N'

        transformed_data.append(d)

    print(transformed_data)

    return transformed_data



def main():
    data = run_extract('0xB8c77482e45F1F44dE1745F52C74426C631bDD52')
    run_transform(data)

if __name__ == '__main__':
    main()


