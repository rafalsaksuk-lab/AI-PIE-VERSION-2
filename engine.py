"""AI Pie stock research only. Signals at close, fills at next session open."""

import math
import pandas as pd

# Last recorded eight-stock AI Growth list; current Trading 212 holdings unverified.
WATCHLIST = {
    "CRDO": "Credo Technology",
    "ALAB": "Astera Labs",
    "COHR": "Coherent",
    "CDNS": "Cadence Design Systems",
    "SNPS": "Synopsys",
    "FN": "Fabrinet",
    "PLTR": "Palantir Technologies",
    "POET": "POET Technologies",
}


def validate_prices(frame):
    required = {"date", "open", "close"}
    if not required.issubset(frame.columns):
        raise ValueError("CSV must contain date, open, close columns.")
    data = frame[list(sorted(required))].copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise", utc=True)
    if (
        data["date"].isna().any()
        or data["date"].duplicated().any()
        or not data["date"].is_monotonic_increasing
    ):
        raise ValueError("Dates must be unique and increasing.")
    for field in ["open", "close"]:
        data[field] = pd.to_numeric(data[field], errors="raise")
        if not data[field].map(lambda x: math.isfinite(x) and x > 0).all():
            raise ValueError("Prices must be finite and positive.")
    if len(data) < 3:
        raise ValueError("At least three sessions are required.")
    return data.set_index("date")


def simulate(prices, window=50, cost_bps=10, initial=1000):
    if not isinstance(window, int) or window < 2 or len(prices) <= window:
        raise ValueError("Window must be at least 2 and shorter than the dataset.")
    if not 0 <= cost_bps <= 500 or not math.isfinite(initial) or not initial > 0:
        raise ValueError("Check costs and starting capital.")
    # Indicators use only information available at the preceding close.
    targets = (prices.close > prices.close.rolling(window).mean()).shift(
        1, fill_value=False
    )
    cost = cost_bps / 10000
    output, ledger = [], []
    cash, shares, benchmark_shares = float(initial), 0.0, 0.0
    # Both comparisons start after identical indicator warm-up.
    for i in range(window, len(prices)):
        date, row = prices.index[i], prices.iloc[i]
        if i == window:
            benchmark_shares = initial / (row.open * (1 + cost))
        target = bool(targets.iloc[i])
        if target and shares == 0:
            shares = cash / (row.open * (1 + cost))
            fee = shares * row.open * cost
            cash = 0.0
            ledger.append(
                {
                    "date": date,
                    "side": "BUY",
                    "price": row.open,
                    "shares": shares,
                    "fee": fee,
                }
            )
        elif not target and shares > 0:
            fee = shares * row.open * cost
            cash = shares * row.open - fee
            ledger.append(
                {
                    "date": date,
                    "side": "SELL",
                    "price": row.open,
                    "shares": shares,
                    "fee": fee,
                }
            )
            shares = 0.0
        output.append(
            {
                "date": date,
                "Strategy": cash + shares * row.close,
                "Buy and hold": benchmark_shares * row.close,
            }
        )
    equity = pd.DataFrame(output).set_index("date")
    return equity, pd.DataFrame(
        ledger, columns=["date", "side", "price", "shares", "fee"]
    )


def metrics(series, initial):
    # Include initial capital so entry fees and first-session loss count in drawdown.
    values = [float(initial)] + series.tolist()
    peak, drawdown = values[0], 0.0
    for value in values:
        peak = max(peak, value)
        drawdown = min(drawdown, value / peak - 1)
    return {
        "Total return (%)": (values[-1] / initial - 1) * 100,
        "Max drawdown (%)": drawdown * 100,
        "Final value": values[-1],
    }
