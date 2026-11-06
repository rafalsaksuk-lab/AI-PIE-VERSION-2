# USD dashboard forward comparison

Simulation only. Independent from the GBP experiment.

Market session: 2026-11-06. Observed at: 2026-11-06T23:07:50Z. Completed sessions: 2 of 20 before review and pause.

| Portfolio | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 995.66 | -4.34 | 0.83 | 4 | 0.50 |
| buy_and_hold | 988.79 | -11.21 | 8.62 | 8 | 1.00 |

Fills: Original SMA50 sold CDNS at 315.50 and SNPS at 449.78 using November 6 daily opening marks, implementing targets durably committed on November 6 at 00:03:11Z, before the 14:30Z open. Benchmark had no new fills.

Pending: Original SMA50 BUY CDNS and BUY SNPS for November 9 regular open at 14:30 UTC. CDNS close 319.92 > SMA50 319.8298; SNPS close 450.46 > SMA50 441.6090. Other six strategy sleeves remain cash. Benchmark holds all eight. Pending actions are not completed fills.

Data checks: 56 complete calendar-aligned daily sessions per symbol; latest 50 used for SMA. All prior snapshot OHLC fields unchanged. No corporate actions returned for August 20–November 9. Zero missing bars or signal sessions. Initial Alpaca requests timed out; retries succeeded before this observation. Raw Alpaca SIP daily basis; no after-hours substitution.

Costs: 0.10% per side, fractional shares, no FX, deposits, rebalancing or cash interest. Maximum drawdown includes initial USD1000 and recorded closing values, not intraday lows. Daily price marks approximate executable fills.

Append-only ledger and source snapshots. Review and pause after 20 completed sessions; continue GBP experiment. No rule tuning. Two sessions cannot establish an edge.
