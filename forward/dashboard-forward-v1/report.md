# USD dashboard forward comparison

Simulation only. Independent from the GBP experiment.

Market session: 2026-11-11. Observed at: 2026-11-11T23:16:10Z. Completed sessions: 5 of 20 before review and pause.

| Portfolio | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 999.17 | -0.83 | 0.83 | 6 | 0.74 |
| buy_and_hold | 1106.76 | 106.76 | 8.62 | 8 | 1.00 |

Fills this session: none. Previously recorded targets maintained existing holdings.
Pending actions for November 12: none. Strategy retains CDNS and SNPS; six other sleeves remain cash. Benchmark retains all eight.
CDNS close 329.26 > SMA50 319.9342; SNPS close 462.12 > SMA50 443.4494.

Data checks: 59 complete calendar-aligned daily sessions per symbol; latest 50 used for SMA. All prior snapshot OHLC unchanged. No corporate actions returned for August 20–November 12. Zero missing bars or signal sessions. Raw Alpaca SIP daily basis; no after-hours substitution.

Costs: 0.10% per side, fractional shares, no FX, deposits, rebalancing or cash interest. Maximum drawdown includes initial USD1000 and recorded closing values, not intraday lows. Daily marks approximate fills.

Append-only ledger and source snapshots. Review and pause after 20 completed sessions; continue GBP experiment. No rule tuning. Five sessions cannot establish an edge.
