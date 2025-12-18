# AI Sentiment & Market Efficacy: An OMSA Research Sample

**Project Overview**: This repository contains an econometric analysis of sentiment signals during the 2025 AI expansion. It focuses on the correlation between product innovation (Gemini 3) and equity price volatility.

### ⚠️ Disclaimer
* **Personal Academic Work**: This project is for educational purposes only (Georgia Tech OMSA).
* **Company Status**: The author is an employee of Google; however, this research uses only **publicly available data** and represents the author's **personal opinions** only.
* **No Inside Info**: No non-public or material financial information was used in this study.
* **Quiet Period**: This project is currently static in observance of the standard quiet period.

### Key Findings
- **Gemini Correlation**: 0.00 (Neutral leading indicator)
- **Corporate Correlation**: -0.23 (Negative regulatory pressure)
- **Alpha**: -10.53% during launch window (Standard "Sell the News" pattern).

### How to Run

1) Clone & enter the repository

```
git clone https://github.com/<your-username>/<repo>.git
cd stock-sentiment-analysis
```

2) Create & activate a virtual environment (recommended)

```
python3 -m venv .venv
source .venv/bin/activate
```

3) Install dependencies

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> **Troubleshooting:** If you see import errors after installing requirements, run:
>
> ```
> python -m pip install matplotlib feedparser alpha_vantage dateparser python-dotenv
> ```

4) Set Alpha Vantage API key (required by `fetch_data.py`)

```
export ALPHAVANTAGE_API_KEY="your_api_key_here"
```

5) Fetch / prepare data

```
python fetch_data.py      # Downloads google stock data
python fetch_news.py      # Collects headlines (alphabet & gemini)
python benchmark.py       # Downloads or creates QQQ benchmark
```

6) Prepare sentiment (NLTK VADER)

```
python -c "import nltk; nltk.download('vader_lexicon')"
python analyze_sentiment.py
```

7) Run analyses & visualizations

```
python final_comparison.py
python event_study.py
python final_correlation.py
```

Notes:
- If running on a headless server, replace `plt.show()` with `plt.savefig('plot.png')` in scripts to save figures instead of displaying interactive windows.
- After verifying, you can update `requirements.txt` with pinned versions: `python -m pip freeze > requirements.txt`