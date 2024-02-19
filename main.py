# Save this script as pixel_price_monitor.py or another name of your choice.

import streamlit as st
import requests

# CoinMarketCap API URL and headers
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
API_KEY = st.secrets['API_KEY']  # Replace with your CoinMarketCap API Key
PARAMS = {
    'slug': 'pixels',  # Use 'symbol': 'PIXEL' if you know the symbol
    'convert': 'USD'
}
HEADERS = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def get_pixel_price():
    """Fetches the current price of Pixel currency from CoinMarketCap."""
    response = requests.get(API_URL, headers=HEADERS, params=PARAMS)
    response_json = response.json()
    # Parsing the response to get the price. Adjust the path according to the actual response structure
    pixel_data = response_json['data']
    for key in pixel_data:
        pixel = pixel_data[key]
        price = pixel['quote']['USD']['price']
        return price

# Streamlit application layout
st.title('Pixel Currency Price Monitor')

if st.button('Refresh Price'):
    price = get_pixel_price()
    if price:
        st.write(f'Current Pixel Price: USD {price:.4f}')
    else:
        st.error('Failed to fetch price. Check your API key and internet connection.')
