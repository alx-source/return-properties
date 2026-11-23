# Empirical properties of stock returns

## Question

Do daily stock returns follow a normal distribution, and are they independent from day to day?

## Data

Daily adjusted closing prices for 50 large US stocks in 11 sectors plus SPY, from 2016-01-01 to 2025-12-31, downloaded from Yahoo Finance with `yfinance`. The prices are saved to `data/prices.csv`, which is not committed.

## How to run

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/analysis.ipynb
```

Run the notebook from top to bottom. The first run downloads the prices (about one minute); later runs read the saved file.

## Findings

1.
2.
3.
