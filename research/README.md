# AI Growth backtest, 4 November 2026

From the repository root with its Python requirements installed, run `python reproduce.py`. This recreates summary.csv and trades.csv offline. Each input contains 461 daily USD open and close observations from Alpaca's consolidated US SIP feed, retrieved 4 November 2026 for 2 January 2025 through 3 November 2026. The feed response did not specify an adjustment basis. Treat these as historical price simulations.

Each period starts fresh with $125 per stock ($1,000 total), fractional shares and no rebalancing across stocks. The dashboard engine calculates the 50-session moving average at the previous close, trades at the next open and charges 0.10% per transaction. Cash earns zero. Buy and hold pays the initial entry cost. Both portfolios are valued at the final close. Drawdown is measured on combined daily equity including starting capital. The trade ledger records strategy fills. To inspect Palantir, filter ticker to PLTR and period_start to 2025-07-14.

During the longer period PLTR made 32 trades. Of 15 completed exits and subsequent repurchases, 12 repurchases occurred at a higher price. PLTR rose 28.6% between the sale on 23 July 2026 and re-entry on 5 August. The selection of eight stocks is retrospective and weights are assumed.
