# USD dashboard forward paper experiment

Simulation only. Two independent USD 1000 portfolios; eight fixed initial USD 125 sleeves.

Market session: 2026-11-12
Observed at: 2026-11-12T23:37:44Z
Completed sessions: 6 of 20. Status: active.

| Strategy | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 1000.86 | 0.86 | 0.83 | 6 | 0.74 |
| buy_and_hold | 1086.85 | 86.85 | 8.62 | 8 | 1.00 |

New simulated fills: none. Pending actions: none for 2026-11-13 open (14:30 UTC).
Original SMA50 retains CDNS and SNPS; the other six sleeves remain cash. Benchmark retains all eight.

Verified Alpaca SIP raw regular daily bars; 60 calendar-matching sessions per symbol; latest 50 complete closes used. Prior OHLC unchanged. No corporate actions returned across lookback through next execution session. No missing signal sessions or data failures.

Costs are cumulative and included in values. Daily opening marks approximate fills, not brokerage executions. No FX, rebalancing, deposits or cash interest. Maximum drawdown includes initial USD 1000. Ledger and snapshots are append-only; no missed targets invented.

Review and pause after 20 completed sessions. Continue separate GBP experiment. This short sample does not establish an edge.
