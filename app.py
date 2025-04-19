import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="StockGEN", layout="centered")
st.title("📈 StockGEN: Smarter Stock Forecasting")

# Layout - Inputs
with st.container():
    st.markdown("### 🎯 Enter Prediction Parameters")
    col1, col2 = st.columns(2)
    with col1:
        stock = st.text_input("🧾 Stock Ticker", value="AAPL", placeholder="e.g., AAPL")
    with col2:
        end_date = st.date_input("🗓️ Select End Date", value=datetime.today())

# Predict button
if st.button("🚀 Predict Now"):
    with st.spinner("🔍 Analyzing market data..."):
        time.sleep(1.5)
        response = requests.post("http://localhost:5000/predict", json={
            "stock": stock,
            "end_date": end_date.strftime("%Y-%m-%d")
        })

        if response.ok:
            result = response.json()

            # Results Display
            st.markdown("## 🧠 Prediction Summary")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("📅 Data Till", result["next_date"])
                st.metric("💼 Ticker", result["ticker"])
                st.metric(f"📉 Predicted Close (after {result["next_date"]})", f"${result['predicted_close']:.2f}")

            with col2:
                st.metric("📊 Trend", result["predicted_trend"])
                st.metric("🎯 Confidence", result["confidence"])
                st.metric("🌪️ Volatility", f"{result['volatility']:.2f}")

            # Styled Recommendation Box
            st.markdown("---")
            st.markdown("### 💡 Final Recommendation")
            recommendation = result["recommendation"]
            color = "green" if recommendation == "Buy" else "red" if recommendation == "Sell" else "orange"
            st.markdown(f"<div style='background-color:{color}; padding:15px; border-radius:10px; text-align:center;'><h3 style='color:white;'>📝 {recommendation}</h3></div>", unsafe_allow_html=True)
        else:
            st.error("❌ Prediction failed. Check server logs.")
