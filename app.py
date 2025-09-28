# xauusd-dashboard
Dashboard analisa XAUUSD dengan Streamlit
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import ta

st.set_page_config(page_title="XAUUSD Dashboard", layout="wide")

# Judul
st.title("📊 XAUUSD AI Dashboard")

# Ambil data XAUUSD
data = yf.download("XAUUSD=X", period="7d", interval="30m")

# Hitung indikator teknikal
data["RSI"] = ta.momentum.RSIIndicator(data["Close"]).rsi()
data["SMA20"] = ta.trend.SMAIndicator(data["Close"], 20).sma_indicator()
data["SMA50"] = ta.trend.SMAIndicator(data["Close"], 50).sma_indicator()

# Tentukan sinyal trading sederhana
last_close = data["Close"].iloc[-1]
last_rsi = data["RSI"].iloc[-1]
signal = "WAIT"
confidence = "MEDIUM"

if last_rsi < 30 and last_close > data["SMA20"].iloc[-1]:
    signal = "LONG"
    confidence = "HIGH"
elif last_rsi > 70 and last_close < data["SMA20"].iloc[-1]:
    signal = "SHORT"
    confidence = "HIGH"

# Chart candlestick
fig = go.Figure(data=[go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="Candlestick"
)])
fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], line=dict(color="blue", width=1), name="SMA20"))
fig.add_trace(go.Scatter(x=data.index, y=data["SMA50"], line=dict(color="orange", width=1), name="SMA50"))

st.plotly_chart(fig, use_container_width=True)

# Kotak informasi
st.subheader("📌 Trading Signal")
st.write(f"**Signal**: {signal}")
st.write(f"**Confidence Level**: {confidence}")
st.write(f"**Last Close**: {last_close:.2f}")
st.write(f"**RSI**: {last_rsi:.2f}")
