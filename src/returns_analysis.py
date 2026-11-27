"""Analysis"""

import os
import time

import numpy as np
import pandas as pd
import yfinance as yf

TICKERS = [
    "AAPL", "MSFT", "NVDA", "ORCL", "CSCO", "INTC", "IBM",
    "GOOGL", "META", "DIS", "VZ", "T",
    "AMZN", "HD", "MCD", "NKE", "SBUX",
    "PG", "KO", "PEP", "WMT", "COST",
    "JPM", "BAC", "GS", "WFC", "AXP",
    "JNJ", "PFE", "UNH", "MRK", "ABT",
    "XOM", "CVX", "COP", "SLB",
    "BA", "CAT", "HON", "UPS", "GE",
    "APD", "SHW", "FCX",
    "NEE", "DUK", "SO",
    "AMT", "PLD", "SPG",
    "SPY",
]
START_DATE = "2016-01-01"
END_DATE = "2025-12-31"

BATCH_SIZE = 10
PAUSE_SECONDS = 5
MAX_RETRIES = 3


def download_batch(tickers, start, end) -> pd.DataFrame:
    """Downloads Adjusted Close (or Close) prices for a single batch of tickers."""
    end_exclusive = pd.Timestamp(end) + pd.Timedelta(days=1)
    # auto_adjust=True adjusts for splits and dividends automatically in 'Close'
    for attempt in range(MAX_RETRIES + 1):
        df = yf.download(
        tickers=tickers,
        start=start,
        end=end_exclusive,
        auto_adjust=True,
        progress=False,
        )
        if len(df) > 0:
            prices = df["Close"]
            if not prices.isna().all().any():
                return prices
        time.sleep(PAUSE_SECONDS)
    raise RuntimeError("Download failed after " + str(MAX_RETRIES) + " retries for: " + ", ".join(tickers))


def download_prices(tickers, start, end, path):
    """Downloads all tickers in batches and saves them to a CSV; loads the file if it already exists."""
    if os.path.exists(path):
        return load_prices(path)

    batches = []
    for first in range(0, len(tickers), BATCH_SIZE):
        batch = tickers[first : first + BATCH_SIZE]
        batches.append(download_batch(batch, start, end))
        time.sleep(PAUSE_SECONDS)

    prices = pd.concat(batches, axis=1)
    prices = prices[tickers]
    prices.index.name = "Date"

    # Fallback to "." prevents FileNotFoundError if path has no folder (e.g., "prices.csv")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    prices.to_csv(path)
    return prices


def load_prices(path):
    prices = pd.read_csv(path, index_col="Date", parse_dates=True)
    return prices


def compute_log_returns(prices):
    """Compute daily log returns from a DataFrame or Series of prices."""
    previous_prices = prices.shift(1)
    log_returns = np.log(prices / previous_prices)
    log_returns = log_returns.iloc[1:]
    return log_returns


def sample_skewness(x):
    """Compute sample skewness from an array or Series of returns."""
    deviations = x - np.mean(x)
    m2 = np.mean(deviations ** 2)
    m3 = np.mean(deviations ** 3)
    return float(m3 / (m2 ** 1.5))


def sample_excess_kurtosis(x):
    """Compute sample excess kurtosis from an array or Series of returns."""
    deviations = x - np.mean(x)
    m2 = np.mean(deviations ** 2)
    m4 = np.mean(deviations ** 4)
    return float(m4 / m2 ** 2 - 3)
