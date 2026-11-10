# USD dashboard forward comparison

Simulation only. Independent from the GBP experiment.

Market session: 2026-11-10. Observed at: 2026-11-10T23:14:14Z. Completed sessions: 4 of 20 before review and pause.

| Portfolio | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 999.48 | -0.52 | 0.83 | 6 | 0.74 |
| buy_and_hold | 1049.32 | 49.32 | 8.62 | 8 | 1.00 |

Fills this session: none. Previously recorded targets maintained existing holdings.
Pending actions for November 11: none. Strategy retains CDNS and SNPS; six other sleeves remain cash. Benchmark retains all eight.
CDNS close 331.64 > SMA50 319.6098; SNPS close 459.95 > SMA50 442.5034.

Data checks: 58 complete calendar-aligned daily sessions per symbol; latest 50 used for SMA. All prior snapshot OHLC unchanged. No corporate actions returned for August 20–November 11. Zero missing bars or signal sessions. Raw Alpaca SIP daily basis; no after-hours substitution. Initial future-end query hit SIP delay limit; completed-close cutoff retry succeeded.

Costs: 0.10% per side, fractional shares, no FX, deposits, rebalancing or cash interest. Maximum drawdown includes initial USD1000 and recorded closing values, not intraday lows. Daily marks approximate fills.

Append-only ledger and source snapshots. Review and pause after 20 completed sessions; continue GBP experiment. No rule tuning. Four sessions cannot establish an edge.
