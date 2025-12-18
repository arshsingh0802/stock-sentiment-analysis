import pandas as pd
import matplotlib.pyplot as plt
import dateparser
import os

# 1. Load both datasets
prices = pd.read_csv('data/google_stock_data.csv')
sentiment = pd.read_csv('data/analyzed_news_sentiment.csv')

# Standardize Column Names to prevent KeyErrors
prices.columns = prices.columns.str.lower()
sentiment.columns = sentiment.columns.str.lower()

# 2. THE FIX: Smart Date Parsing
# Translates "1 hour ago" or "Dec 17, 2025" into a standard date object
def smart_date_parser(date_str):
    parsed = dateparser.parse(str(date_str))
    return parsed.date() if parsed else None

print("🤖 Translating relative news times (e.g., '1 hour ago')...")
sentiment['date'] = sentiment['date'].apply(smart_date_parser)
prices['date'] = pd.to_datetime(prices['date']).dt.date

# 3. Aggregate Sentiment (Average score per day)
daily_sentiment = sentiment.groupby('date')['sentiment_score'].mean().reset_index()

# 4. Merge the data using a 'left' join
# This keeps all price data even if no news exists for that day
merged = pd.merge(prices, daily_sentiment, on='date', how='left')
merged['sentiment_score'] = merged['sentiment_score'].fillna(0) # Fill missing days with Neutral (0)

if merged.empty:
    print("⚠️ Still no matching dates. Check if data/ folder has the correct files.")
else:
    # 5. Visualize
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Stock Price (USD)', color='blue')
    ax1.plot(merged['date'], merged['close'], color='blue', marker='o', label='Stock Price')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Sentiment Score', color='red')
    ax2.bar(merged['date'], merged['sentiment_score'], color='red', alpha=0.3, label='Sentiment')
    
    plt.title('Google Stock Price vs. News Sentiment (Smart Parsed)')
    plt.tight_layout()
    plt.show()

    # 6. Final Result
    corr = merged['close'].corr(merged['sentiment_score'])
    print(f"\n📊 Final Correlation Coefficient: {corr:.2f}")
