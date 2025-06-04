import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_screener_data(stock_name):
    url = f"https://www.screener.in/company/{stock_name.upper()}/"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"id": "profit-loss"})
        if not table:
            return None

        headers = [th.text.strip() for th in table.find_all("th")]
        rows = table.find_all("tr")
        data = []
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) == len(headers):
                label = cols[0].text.strip()
                values = [col.text.strip().replace(",", "") for col in cols[1:]]
                data.append([label] + values)

        df = pd.DataFrame(data, columns=["Metric"] + headers[1:])
        df.set_index("Metric", inplace=True)
        return df.T
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
