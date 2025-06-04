import pandas as pd

def calculate_valuation(screener_df, year, depreciation, tax_rate):
    try:
        tax_decimal = tax_rate / 100
        if str(year) not in screener_df.index:
            return pd.DataFrame([{"Error": f"Year {year} not available in Screener data."}])

        row = screener_df.loc[str(year)]
        sales = float(row.get("Sales", 0))
        ebitda = float(row.get("Operating Profit", 0))
        other_income = float(row.get("Other Income", 0))
        interest = float(row.get("Interest", 0))

        pbt = ebitda + other_income - depreciation - interest
        tax = pbt * tax_decimal
        pat = pbt - tax
        cash_flow = pat + depreciation
        cfo_ebitda = (cash_flow / ebitda) if ebitda != 0 else 0

        return pd.DataFrame([{
            "Year": year,
            "Sales (₹ Cr)": round(sales, 2),
            "EBITDA (₹ Cr)": round(ebitda, 2),
            "PBT (₹ Cr)": round(pbt, 2),
            "Tax (₹ Cr)": round(tax, 2),
            "PAT (₹ Cr)": round(pat, 2),
            "Cash Flow (₹ Cr)": round(cash_flow, 2),
            "CFO/EBITDA": round(cfo_ebitda, 2),
        }])
    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])
