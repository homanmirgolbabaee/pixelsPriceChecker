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

@st.cache_data(ttl=300)  # Cache data for 5 minutes to minimize API calls
def get_pixel_data(convert='USD'):
    """Fetches the current data of Pixel currency from CoinMarketCap."""
    params = {
        'slug': 'pixels',  # Use 'symbol': 'PIXEL' if you know the symbol
        'convert': convert
    }
    response = requests.get(API_URL, headers=HEADERS, params=params)
    response_json = response.json()
    pixel_data = response_json['data']
    for key in pixel_data:
        pixel = pixel_data[key]
        price = pixel['quote'][convert]['price']
        percent_change_24h = pixel['quote'][convert]['percent_change_24h']
        market_cap = pixel['quote'][convert]['market_cap']
        volume_24h = pixel['quote'][convert]['volume_24h']
        return price, percent_change_24h, market_cap, volume_24h

# Simulated function to fetch historical price data (for demonstration)
@st.cache_data(ttl=3600)  # Cache this for 1 hour
def get_historical_prices(convert='USD'):
    # Generate a DataFrame with simulated historical data for the past 7 days
    today = datetime.datetime.now()
    dates = [today - datetime.timedelta(days=i) for i in range(7)]
    prices = np.random.uniform(low=100, high=200, size=7)  # Simulated prices
    return pd.DataFrame({'Date': dates, 'Price': prices})

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
        
        # Fetch and plot historical price data
        historical_prices = get_historical_prices(convert=currency_option)
        st.line_chart(historical_prices.set_index('Date')['Price'])
    else:
        st.error('Failed to fetch data. Check your API key and internet connection.')
