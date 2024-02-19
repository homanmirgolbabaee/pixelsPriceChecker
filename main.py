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

def get_pixel_data(convert='USD'):
    """Fetches the current data of Pixel currency from CoinMarketCap."""
    params = {
        'slug': 'pixels',  # Use 'symbol': 'PIXEL' if you know the symbol
        'convert': convert
    }
    response = requests.get(API_URL, headers=HEADERS, params=params)
    response_json = response.json()
    # Parsing the response to get data. Adjust the path according to the actual response structure
    pixel_data = response_json['data']
    for key in pixel_data:
        pixel = pixel_data[key]
        price = pixel['quote'][convert]['price']
        percent_change_24h = pixel['quote'][convert]['percent_change_24h']
        market_cap = pixel['quote'][convert]['market_cap']
        volume_24h = pixel['quote'][convert]['volume_24h']
        return price, percent_change_24h, market_cap, volume_24h

# Streamlit application layout
st.title('Pixel Currency Price Monitor')

currency_option = st.selectbox('Choose the currency:', ('USD', 'EUR', 'JPY', 'GBP'))

if st.button('Refresh Data'):
    price, percent_change_24h, market_cap, volume_24h = get_pixel_data(convert=currency_option)
    if price:
        st.metric(label="Current Price", value=f"{currency_option} {price:.4f}")
        st.metric(label="24h Change", value=f"{percent_change_24h:.2f}%")
        st.metric(label="Market Cap", value=f"{currency_option} {market_cap:.2f}")
        st.metric(label="24h Volume", value=f"{currency_option} {volume_24h:.2f}")
    else:
        st.error('Failed to fetch data. Check your API key and internet connection.')
