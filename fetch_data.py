import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

# 1. Setup folder
if not os.path.exists('data'):
    os.makedirs('data')

# 2. Setup your API Key (read from environment)
API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
if not API_KEY:
    # Try optional .env file if python-dotenv is available
    try:
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    except Exception:
        pass

if not API_KEY:
    raise RuntimeError(
        "ALPHAVANTAGE_API_KEY not found. Set it in the environment or in a .env file."
    )

print("🚀 Attempting stable data fetch via Alpha Vantage (Standard Mode)...")

try:
    ts = TimeSeries(key=API_KEY, output_format='pandas')
    
    # We removed 'outputsize=full' to stay on the Free Tier.
    # By default, Alpha Vantage returns the last 100 trading days.
    data, meta_data = ts.get_daily(symbol='GOOGL')
    
    # Clean column names (removing the numbers like '1. open')
    data.columns = [col.split('. ')[1] for col in data.columns]
    
    # Save the data
    data.to_csv('data/google_stock_data.csv')
    
    print(f"✅ Success! Downloaded the latest {len(data)} trading days.")
    print("File saved to: data/google_stock_data.csv")

except Exception as e:
    print(f"⚠️ Alpha Vantage Error: {e}")
    print("💡 TIP: If you just ran this, wait 60 seconds (Free tier limit).")
