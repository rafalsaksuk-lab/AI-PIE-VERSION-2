"""Rebuild the two dated AI Growth portfolio experiments from frozen daily bars."""

from pathlib import Path

import pandas as pd

from engine import WATCHLIST, metrics, simulate, validate_prices

ROOT = Path(__file__).resolve().parent / "research"
PERIODS = [
    ("2025-03-18", "2025-07-11", 80),
    ("2025-07-14", "2026-11-03", 331),
]


def main():
    summaries, ledgers = [], []
    for start, end, sessions in PERIODS:
        portfolio = None
        for ticker in WATCHLIST:
            raw = pd.read_csv(ROOT / "inputs" / f"{ticker}.csv")
            if not raw.ticker.eq(ticker).all():
                raise ValueError(f"Unexpected symbol in {ticker} input")
            prices = validate_prices(raw)
            first = prices.index.get_loc(pd.Timestamp(start, tz="UTC"))
            last = prices.index.get_loc(pd.Timestamp(end, tz="UTC"))
            if first < 50 or last - first + 1 != sessions:
                raise ValueError(f"Incomplete {ticker} history for {start}")
            equity, trades = simulate(prices.iloc[first - 50 : last + 1], 50, 10, 125)
            if portfolio is not None and not portfolio.index.equals(equity.index):
                raise ValueError(f"Session mismatch for {ticker}")
            portfolio = equity if portfolio is None else portfolio + equity
            ledgers.append(trades.assign(period_start=start, ticker=ticker))
        for strategy in portfolio:
            summaries.append(
                dict(
                    start=start,
                    end=end,
                    sessions=sessions,
                    strategy=strategy,
                    **metrics(portfolio[strategy], 1000),
                )
            )
    pd.DataFrame(summaries).to_csv(
        ROOT / "summary.csv", index=False, float_format="%.8f"
    )
    trades = pd.concat(ledgers).sort_values(["period_start", "date", "ticker"])
    trades.to_csv(ROOT / "trades.csv", index=False, float_format="%.8f")


if __name__ == "__main__":
    main()
