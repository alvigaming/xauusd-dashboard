import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator

# Konfigurasi halaman
st.set_page_config(page_title="XAUUSD Dashboard", layout="wide")
st.title("📊 XAUUSD AI Dashboard")

# =============================
# Ambil data XAUUSD dari Yahoo Finance
# =============================
symbol = st.selectbox("Pilih Symbol", ["XAUUSD", "GC=F", "GLD"])
interval = st.selectbox("Pilih Interval", ["1M", "15m", "30m", "60m", "1d"])

data = yf.download(symbol, period="5d", interval=interval)

# Cek kalau data kosong
if data.empty:
    st.error("⚠️ Data XAUUSD tidak tersedia. Coba ganti interval/period atau cek koneksi internet.")
    st.stop()

# Kalau kolomnya MultiIndex (kadang terjadi di yfinance intraday)
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

# Pastikan kolom Close berupa float 1D
data["Close"] = data["Close"].astype(float)

# =============================
# Hitung indikator teknikal
# =============================
data["RSI"] = RSIIndicator(close=data["Close"], window=14).rsi()
data["SMA20"] = SMAIndicator(close=data["Close"], window=20).sma_indicator()
data["SMA50"] = SMAIndicator(close=data["Close"], window=50).sma_indicator()

# =============================
# Chart harga emas
# =============================
fig = go.Figure()

# Candlestick chart
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data["Open"],
    high=data["High"],
    low=data["Low"],
    close=data["Close"],
    name="XAU/USD"
))

# Tambahkan SMA20 & SMA50
fig.add_trace(go.Scatter(x=data.index, y=data["SMA20"], 
                         line=dict(color="blue"), name="SMA20"))
fig.add_trace(go.Scatter(x=data.index, y=data["SMA50"], 
                         line=dict(color="red"), name="SMA50"))

st.plotly_chart(fig, use_container_width=True)

# =============================
# Sinyal trading sederhana
# =============================
current_price = round(data["Close"].iloc[-1], 2)
entry = current_price
sl = round(current_price - 6, 2)
tp = round(current_price + 12, 2)

st.subheader("🤖 Rekomendasi Trading")
st.write(f"""
💰 **Current Price**: {current_price}  
🟢 **Entry**: {entry}  
🔴 **Stop Loss**: {sl}  
🟢 **Take Profit**: {tp}  
⚖️ **Risk Reward**: 1:2  
📊 **Confidence Level**: MEDIUM-HIGH  
""")

# =============================
# Analisa RSI
# =============================
rsi = data["RSI"].iloc[-1]

st.subheader("📈 Analisa RSI")
if rsi < 30:
    st.success(f"RSI {rsi:.2f} → Oversold → Potensi BUY 🚀")
elif rsi > 70:
    st.error(f"RSI {rsi:.2f} → Overbought → Potensi SELL 📉")
else:
    st.info(f"RSI {rsi:.2f} → Market netral → Tunggu konfirmasi ⚖️")
