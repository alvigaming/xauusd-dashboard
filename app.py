import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

# Ambil data
data = yf.download("XAUUSD=X", period="5d", interval="30m")

# Kalau kolomnya MultiIndex → turunin level
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Hitung indikator
data["RSI"] = RSIIndicator(close=data["Close"], window=14).rsi()
data["SMA20"] = SMAIndicator(close=data["Close"], window=20).sma_indicator()
data["SMA50"] = SMAIndicator(close=data["Close"], window=50).sma_indicator()

# Chart harga emas
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"], high=data["High"],
    low=data["Low"], close=data["Close"],
    name="XAU/USD"
))
fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], line=dict(color="blue"), name="SMA20"))
fig.add_trace(go.Scatter(x=data.index, y=data["SMA50"], line=dict(color="red"), name="SMA50"))

st.plotly_chart(fig, use_container_width=True)

# Sinyal trading sederhana
current_price = data["Close"].iloc[-1]
entry = round(current_price, 2)
sl = round(current_price - 6, 2)
tp = round(current_price + 12, 2)

st.subheader("🔥 Rekomendasi Trading")
st.write(f"""
💰 **Current Price**: {entry}  
📍 **Entry**: {entry}  
🛑 **Stop Loss**: {sl}  
🎯 **Take Profit**: {tp}  
⚖️ **Risk Reward**: 1:2  
✅ **Confidence Level**: MEDIUM-HIGH  
""")

# Analisa RSI
rsi = data["RSI"].iloc[-1]
if rsi < 30:
    st.success("RSI oversold → Potensi BUY 🚀")
elif rsi > 70:
    st.error("RSI overbought → Potensi SELL 📉")
else:
    st.info("Market netral → Tunggu konfirmasi ⚖️")
