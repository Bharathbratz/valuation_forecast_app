# valuation_forecast_app/model.py
import pandas as pd

def calculate_valuation(screener_data, depreciation):
    try:
        # Extract necessary values (examples shown below)
        sales = float(screener_data.get("Sales", "0").replace(",", ""))
        ebitda_margin = float(screener_data.get("EBITDA Margin", "0").replace("%", "")) / 100
        other_income = float(screener_data.get("Other income", "0").replace(",", ""))
        interest = float(screener_data.get("Interest", "0").replace(",", ""))
        tax_rate = 0.25  # fixed tax assumption

        ebitda = sales * ebitda_margin
        pbt = ebitda + other_income - depreciation - interest
        tax = pbt * tax_rate
        pat = pbt - tax

        cash_flow = pat + depreciation
        cfo_ebitda = (cash_flow / ebitda) if ebitda != 0 else 0

        # Pack results into dataframe
        results = pd.DataFrame([{
            "Sales (₹ Cr)": round(sales, 2),
            "EBITDA (₹ Cr)": round(ebitda, 2),
            "PBT (₹ Cr)": round(pbt, 2),
            "Tax (₹ Cr)": round(tax, 2),
            "PAT (₹ Cr)": round(pat, 2),
            "Cash Flow (₹ Cr)": round(cash_flow, 2),
            "CFO/EBITDA": round(cfo_ebitda, 2),
        }])

        return results

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])
