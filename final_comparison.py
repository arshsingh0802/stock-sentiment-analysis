import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. DATA LOADING & CLEANING ---
def load_and_prep(path):
    if not os.path.exists(path): return None
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    # Handle different date formats (yfinance vs direct CSV)
    df['date'] = pd.to_datetime(df['date'], utc=True).dt.date
    return df

# Load all three files
prices = load_and_prep('data/google_stock_data.csv')
gemini_sent = load_and_prep('data/gemini_sentiment_150.csv')
corp_sent = load_and_prep('data/alphabet_sentiment_150.csv') # Your original corporate file
qqq = load_and_prep('data/qqq_stock_data.csv')

# --- 2. THE COMPARATIVE ANALYSIS (AI vs. CORPORATE) ---
if prices is not None:
    # Prepare Gemini (AI) Sentiment
    gem_daily = gemini_sent.groupby('date')['sentiment_score'].sum().reset_index()
    # Prepare Corporate Sentiment
    corp_daily = corp_sent.groupby('date')['sentiment_score'].sum().reset_index()
    
    # Merge both into prices
    final_df = pd.merge(prices, gem_daily, on='date', how='left').fillna(0)
    final_df = pd.merge(final_df, corp_daily, on='date', how='left', suffixes=('_gem', '_corp')).fillna(0)
    
    # Calculate Returns & Lagged Correlations
    final_df['returns'] = final_df['close'].pct_change()
    corr_gem = final_df['returns'].corr(final_df['sentiment_score_gem'].shift(1))
    corr_corp = final_df['returns'].corr(final_df['sentiment_score_corp'].shift(1))

    # --- DIAGRAM 1: THE COMPARISON ---
    plt.figure(figsize=(14, 7))
    plt.plot(final_df['date'], final_df['close'], color='black', label='GOOGL Price', lw=1, alpha=0.5)
    plt.fill_between(final_df['date'], final_df['sentiment_score_gem'] * 10, color='green', alpha=0.3, label=f'Gemini Sentiment (r={corr_gem:.2f})')
    plt.fill_between(final_df['date'], final_df['sentiment_score_corp'] * 10, color='red', alpha=0.2, label=f'Corporate Sentiment (r={corr_corp:.2f})')
    plt.title("OMSA Analysis: AI Innovation vs. Corporate News Sentiment")
    plt.legend(); plt.grid(alpha=0.2); plt.show()

# --- 3. THE EVENT STUDY (ALPHA) ---
if prices is not None and qqq is not None:
    # Re-calculate Alpha using Price vs. Market Benchmark
    prices['ret_goog'] = prices['close'].pct_change()
    qqq_col = 'close' if 'close' in qqq.columns else 'adj close'
    qqq['ret_qqq'] = qqq[qqq_col].pct_change()
    
    comp = pd.merge(prices[['date', 'ret_goog']], qqq[['date', 'ret_qqq']], on='date')
    comp['alpha'] = comp['ret_goog'] - comp['ret_qqq']
    
    # Analyze the "Gemini 3 Launch" Window
    event_date = pd.to_datetime('2025-11-18').date()
    window = comp[(comp['date'] >= event_date - pd.Timedelta(days=2)) & 
                  (comp['date'] <= event_date + pd.Timedelta(days=5))].copy()
    window['cum_alpha'] = (1 + window['alpha']).cumprod() - 1

    plt.figure(figsize=(10, 5))
    plt.plot(window['date'], window['cum_alpha'] * 100, color='blue', lw=3, label='Cumulative Alpha (%)')
    plt.axhline(0, color='black', linestyle='--')
    plt.axvline(event_date, color='red', linestyle=':', label='Gemini 3 Launch')
    plt.title("Event Study: Abnormal Returns During Gemini 3 Launch")
    plt.ylabel('Alpha (%) vs QQQ'); plt.legend(); plt.show()

    print(f"✅ Analysis Complete.")
    print(f"📊 Gemini Correlation: {corr_gem:.2f}")
    print(f"📊 Corporate Correlation: {corr_corp:.2f}")
    print(f"📊 Launch Window Alpha: {window['cum_alpha'].iloc[-1]*100:.2f}%")
