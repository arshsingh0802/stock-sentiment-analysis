import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# 1. Setup VADER with Financial Weights
analyzer = SentimentIntensityAnalyzer()

# CUSTOM FINANCIAL DICTIONARY: Teaching VADER about the market
# Weights range from -4.0 (worst) to +4.0 (best)
financial_lexicon = {
    'gemini': 2.5,      # Strategic AI product
    'ai': 1.5,          # Sector growth
    'beat': 2.0,        # Performance vs. expectations
    'beats': 2.0,
    'breakout': 3.0,    # Strong technical upward movement
    'rally': 3.0,       # Sustained price increase
    'upgraded': 2.0,    # Analyst positive rating
    'buy': 2.0,         # Investment recommendation
    'growth': 1.5,
    'innovation': 1.5,
    'leads': 1.5,
    'dominates': 2.0,
    'antitrust': -2.5,  # Specific legal risk for Google
    'regulation': -1.5,
    'threat': -2.0,
    'competition': -1.0,
    'miss': -2.5,       # Earnings failure
    'downgrade': -3.0   # Analyst negative rating
}

analyzer.lexicon.update(financial_lexicon)
print("⚙️ VADER lexicon updated with 150-day financial context.")

# 2. Function to analyze a single file
def process_sentiment(input_filename, output_filename):
    input_path = f'data/{input_filename}'
    
    if not os.path.exists(input_path):
        print(f"⚠️ Warning: {input_filename} not found. Skipping...")
        return

    print(f"🤖 Analyzing sentiment for: {input_filename}...")
    df = pd.read_csv(input_path)

    # Calculate 'Compound' score (the normalized, weighted composite)
    df['sentiment_score'] = df['title'].apply(
        lambda x: analyzer.polarity_scores(str(x))['compound'] if pd.notna(x) else 0
    )

    # Categorize for reporting purposes
    df['label'] = df['sentiment_score'].apply(
        lambda s: 'POSITIVE' if s > 0.05 else ('NEGATIVE' if s < -0.05 else 'NEUTRAL')
    )

    # Save to the specific analyzed file name
    output_path = f'data/{output_filename}'
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Saved to {output_path}")

# 3. RUN ANALYSIS ON BOTH DATASETS
# This ensures both Alphabet and Gemini are analyzed with the same rules
process_sentiment('alphabet_news_150.csv', 'alphabet_sentiment_150.csv')
process_sentiment('gemini_news_150.csv', 'gemini_sentiment_150.csv')

print("\n🚀 Analysis complete. Ready for final_comparison.py!")
