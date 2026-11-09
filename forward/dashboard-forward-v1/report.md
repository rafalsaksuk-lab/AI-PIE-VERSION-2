# USD dashboard forward comparison

Simulation only. Independent from the GBP experiment.

Market session: 2026-11-09. Observed at: 2026-11-09T23:29:43Z. Completed sessions: 3 of 20 before review and pause.

| Portfolio | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 1003.22 | 3.22 | 0.83 | 6 | 0.74 |
| buy_and_hold | 1075.75 | 75.75 | 8.62 | 8 | 1.00 |

Fills: Original SMA50 bought CDNS at 324.73 and SNPS at 454.54 using November 9 daily opening marks. Targets were durably committed at 2026-11-06T23:08:54Z before today's open. Benchmark had no new fills.

Pending actions for November 10: none. Strategy retains CDNS and SNPS; other six sleeves remain cash. Benchmark retains all eight. CDNS close 336.53 > SMA50 319.7526; SNPS close 466.97 > SMA50 442.0962.

Data checks: 57 complete calendar-aligned daily sessions per symbol; latest 50 used for SMA. Prior snapshot OHLC unchanged. No corporate actions returned for August 20–November 10. Zero missing bars or signal sessions. Raw Alpaca SIP daily basis; no after-hours substitution.

Costs: 0.10% per side, fractional shares, no FX, deposits, rebalancing or cash interest. Maximum drawdown includes initial USD1000 and recorded closing values, not intraday lows. Daily price marks approximate executable fills.

Append-only ledger and source snapshots. Review and pause after 20 completed sessions; continue GBP experiment. No rule tuning. Three sessions cannot establish an edge.
