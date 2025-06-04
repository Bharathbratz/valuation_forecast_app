import streamlit as st
import pandas as pd
from screener_fetch import fetch_screener_data
from model import calculate_valuation

st.set_page_config(page_title="Valuation Forecast Tool", layout="centered")
st.title("📊 Equity Valuation Forecast App")

st.sidebar.header("Enter Stock Details")
stock_name = st.sidebar.text_input("Stock Name (as on Screener.in)", "TCS")
current_year = st.sidebar.number_input("Current Year (e.g. 2023)", min_value=2000, max_value=2100, value=2023)

st.sidebar.header("User Inputs (X)")
depreciation = st.sidebar.number_input("Depreciation (₹ Cr)", min_value=0.0, value=100.0)
tax_rate = st.sidebar.slider("Tax Rate (%)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)

if st.button("Run Forecast"):
    with st.spinner("Fetching Screener data and calculating projections..."):
        screener_data = fetch_screener_data(stock_name)
        if screener_data is None:
            st.error("Could not fetch data from Screener.in. Please check the stock name.")
        else:
            results_df = calculate_valuation(screener_data, current_year, depreciation, tax_rate)

            st.success("Forecast completed!")
            st.dataframe(results_df)

            csv = results_df.to_csv(index=False)
            st.download_button("📥 Download Forecast (CSV)", csv, file_name="valuation_forecast.csv")
else:
    st.info("Enter stock name, current year, depreciation, and tax rate, then click 'Run Forecast'")
