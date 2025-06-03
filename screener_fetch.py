# valuation_forecast_app/screener_fetch.py
import requests
from bs4 import BeautifulSoup
import re

def fetch_screener_data(stock_name):
    url = f"https://www.screener.in/company/{stock_name.upper()}/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        data = {}

        # Example Screener tags to scrape
        stats = soup.select(".company-ratios .flex.flex-space-between")
        for stat in stats:
            label = stat.select_one(".name")
            value = stat.select_one(".value")
            if label and value:
                data[label.text.strip()] = value.text.strip()

        # Additional clean-up or parsing if needed
        return data

    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
