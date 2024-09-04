import streamlit as st
from pycoingecko import CoinGeckoAPI
import pandas as pd
import matplotlib.pyplot as plt

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Streamlit page title
st.title("Bitcoin and Ethereum Price Tracker")

# Select cryptocurrency
cryptocurrency = st.selectbox(
    "Select Cryptocurrency",
    ("Bitcoin (BTC)", "Ethereum (ETH)")
)

# Select time range
time_range = st.selectbox(
    "Select Time Range",
    ("1 Hour", "24 Hours", "7 Days")
)

# Map selection to CoinGecko API parameters
if cryptocurrency == "Bitcoin (BTC)":
    crypto_id = "bitcoin"
elif cryptocurrency == "Ethereum (ETH)":
    crypto_id = "ethereum"

if time_range == "1 Hour":
    days = "1"
elif time_range == "24 Hours":
    days = "1"
elif time_range == "7 Days":
    days = "7"

# Fetch market data
data = cg.get_coin_market_chart_by_id(id=crypto_id, vs_currency='usd', days=days)

# Extract price data
prices = data['prices']
df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='ms')
df.set_index('Timestamp', inplace=True)

# Display data table
st.write("Price Data:", df)

# Plot price trend
st.subheader(f"{cryptocurrency} Price Trend ({time_range})")
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Price'], label=f"{cryptocurrency} Price")
plt.xlabel("Time")
plt.ylabel("Price (USD)")
plt.title(f"{cryptocurrency} Price Trend ({time_range})")
plt.legend()
st.pyplot(plt)
