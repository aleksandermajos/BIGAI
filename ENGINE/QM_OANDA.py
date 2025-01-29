import requests

# Replace with your OANDA API key and account details
API_KEY = '2e24a6eb1fbf50c910815785a1d5be04-9e9af28920c69a0de35afd965d9804b9'
ACCOUNT_ID = '101-004-4277345-001'
OANDA_URL = 'https://api-fxpractice.oanda.com/v3'  # For demo accounts
# Use 'https://api-fxtrade.oanda.com/v3' for live accounts

# Define the endpoint for prices
endpoint = f"{OANDA_URL}/accounts/{ACCOUNT_ID}/pricing"

# Define the query parameters
params = {
    "instruments": "EUR_USD"  # Specify the currency pair
}

# Set the request headers
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Make the GET request to OANDA
response = requests.get(endpoint, headers=headers, params=params)

# Parse and display the response
if response.status_code == 200:
    data = response.json()
    prices = data['prices'][0]  # Extract the first price entry
    bid = prices['bids'][0]['price']  # Get bid price
    ask = prices['asks'][0]['price']  # Get ask price

    print(f"EUR/USD Bid Price: {bid}")
    print(f"EUR/USD Ask Price: {ask}")
else:
    print("Error:", response.status_code, response.text)