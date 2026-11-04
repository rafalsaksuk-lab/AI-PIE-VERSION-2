# AI PIE VERSION 2

Independent AI Growth stock research prototype. No crypto, broker connection or order execution. Existing trading212-demo-bot is unaffected.

## Run

Requires Python 3.11+ on a computer or server; view the app through a browser.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## First experiment

The app opens with invented demonstration prices. They are not current market data and are not ASML prices. Select Upload historical CSV for real research. The watchlist uses the last recorded eight-stock AI Growth list: CRDO, ALAB, COHR, CDNS, SNPS, FN, PLTR, POET. This is historical context, not a verification of current Trading 212 holdings or weights. Core and standalone holdings are excluded. Each stock can be tested separately; a combined weighted Pie backtest is not yet implemented. Ticker selection is a label, not a data downloader.

CSV columns: `date,open,close`. Dates must be increasing and unique. Use daily AI Growth stock prices in one currency with open and close on the same split/dividend-adjusted basis. Do not mix adjusted close with unadjusted open. Keep provider and retrieval-date records. Missing exchange sessions and correct adjustments cannot be established from these columns alone.

Signals are calculated at the previous close; transactions fill at the next provided session open. Strategy and benchmark start after the same moving-average warm-up. Fractional shares, zero interest on cash, proportional transaction costs, no taxes or FX; final holdings marked to market without a forced exit. Returns include entry costs. This prototype is in-sample research and does not demonstrate profitability.

## Verification

```bash
python -m unittest discover -s tests -v
```

## Next milestones

1. Verified historical equity/ETF data adapter with source timestamps and calendar checks.
2. Frozen training/test split and untouched out-of-sample comparison.
3. Backtesting.py cross-check and QuantStats reports, after dependency compatibility checks.
4. Portfolio comparisons and optional prospective paper ledger.

The first version has a small transparent simulation engine. Backtesting.py and QuantStats are planned integrations, not installed features. No scheduling, live trading, deployment or changes to the existing bot are included.

## Automated checks

Install `requirements-dev.txt`, then run `python -m ruff check .`, `python -m ruff format --check .`, `python -m coverage run -m pytest -q`, and `python -m coverage report`. GitHub Actions repeats these on Python 3.11 and 3.12 for pushes and pull requests and saves test/coverage artifacts. Coverage measures exercised code, not investment reliability.

Tools used: pytest (tests), Streamlit AppTest (dashboard interaction), Coverage.py (engine coverage), Ruff (code checks), GitHub Actions (automation). Backtesting.py and QuantStats remain future independent cross-check/report integrations. This version does not yet aggregate all eight stocks into a weighted portfolio.
