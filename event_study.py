import pandas as pd
import matplotlib.pyplot as plt

# Load GOOGL and QQQ Data
googl = pd.read_csv('data/google_stock_data.csv')
qqq = pd.read_csv('data/qqq_stock_data.csv') # You'll need to fetch this!

for df in [googl, qqq]:
    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['ret'] = df['close'].pct_change()

# Merge and calculate Abnormal Return (AR)
comparison = pd.merge(googl[['date', 'ret']], qqq[['date', 'ret']], on='date', suffixes=('_goog', '_qqq'))
comparison['abnormal_ret'] = comparison['ret_goog'] - comparison['ret_qqq']

# Event Window: Nov 18 Launch
event_date = pd.to_datetime('2025-11-18').date()
window = comparison[(comparison['date'] >= event_date - pd.Timedelta(days=2)) & 
                    (comparison['date'] <= event_date + pd.Timedelta(days=5))].copy()

window['cum_abnormal'] = (1 + window['abnormal_ret']).cumprod() - 1

# --- VISUALIZATION ---
plt.figure(figsize=(10, 5))
plt.plot(window['date'], window['cum_abnormal'] * 100, label='Alpha (GOOGL vs QQQ)', color='blue', lw=3)
plt.axhline(0, color='red', linestyle='--')
plt.title('Abnormal Returns: Did Google beat the Market during Gemini 3 Launch?')
plt.ylabel('Outperformance %')
plt.legend()
plt.show()

print(f"📊 Final Abnormal Return: {window['cum_abnormal'].iloc[-1]*100:.2f}%")
