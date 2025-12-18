import feedparser
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import urllib.parse

def fetch_historical_rss(keyword, filename):
    print(f"🚀 Starting High-Volume Fetch for: {keyword}")
    all_news = []
    
    # 150-day window from Aug 1 to Dec 17, 2025
    current_date = datetime(2025, 8, 1)
    end_date = datetime(2025, 12, 17)
    
    while current_date < end_date:
        next_date = current_date + timedelta(days=7)
        
        # Broad keywords ensure we capture the full narrative
        # Use quotes for exact matches but remove "NOT" filters to prevent data loss
        date_query = f"after:{current_date.strftime('%Y-%m-%d')} before:{next_date.strftime('%Y-%m-%d')}"
        full_query = f"{keyword} {date_query}"
        
        encoded_query = urllib.parse.quote(full_query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
        
        print(f"  📅 Fetching week of {current_date.strftime('%b %d')}...")
        
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                all_news.append({
                    'date': entry.published,
                    'title': entry.title,
                    'link': entry.link,
                    'source': entry.source.title if hasattr(entry, 'source') else "Unknown"
                })
            time.sleep(1.5) # Gentle rate limit
        except Exception as e:
            print(f"    ⚠️ Error: {e}")
        
        current_date = next_date

    if all_news:
        df = pd.DataFrame(all_news)
        df = df.drop_duplicates(subset=['title'])
        if not os.path.exists('data'): os.makedirs('data')
        df.to_csv(f'data/{filename}', index=False)
        print(f"✅ SUCCESS: Saved {len(df)} unique headlines to data/{filename}\n")

# --- EXECUTION ---
# Group 1: Corporate signals (Alphabet focus)
fetch_historical_rss('Alphabet Inc GOOGL stock', 'alphabet_news_150.csv')

# Group 2: Product signals (AI focus)
fetch_historical_rss('Google Gemini AI benchmark', 'gemini_news_150.csv')
