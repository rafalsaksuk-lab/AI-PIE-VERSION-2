# USD dashboard forward comparison

Simulation only. Independent from the GBP experiment.

Market session: 2026-11-05. Observed at: 2026-11-06T00:02:49Z. Completed sessions: 1 of 20 before review and pause.

| Portfolio | Value USD | Profit USD | Max drawdown % | Trades | Costs USD |
|---|---:|---:|---:|---:|---:|
| original_sma50 | 991.73 | -8.27 | 0.83 | 2 | 0.25 |
| buy_and_hold | 913.75 | -86.25 | 8.62 | 8 | 1.00 |

Fills: original SMA50 bought CDNS and SNPS; benchmark bought all eight, using the 5 November daily opening marks. These implement seed targets durably recorded in the 5 November 00:07 UTC checkpoint before the open; they are not backfilled signals.

Pending: original SMA50 SELL CDNS and SELL SNPS for 6 November 2026 regular open (14:30 UTC). All eight latest close/SMA50 targets are cash; other six strategy sleeves remain cash. Benchmark holds all eight. Pending actions are not fills.

Data checks: 55 calendar-aligned complete daily sessions per symbol, latest 50 used for SMA; all seed close/SMA50 values reproduced; no corporate actions returned for 20 August–6 November; zero missing bars or signal sessions. Raw Alpaca SIP daily basis. Daily and minute bars have different trade-condition filters; the frozen daily marks are used. No after-hours price substitution.

Costs: 0.10% each side; fractional shares; no FX, deposits, rebalancing or cash interest. Drawdown includes initial USD1000 and recorded closing values, not intraday lows. These are approximate paper fills, not real money earned or lost. One session establishes no trading edge.

Read protocol.json and ledger/ before each run. Ledger and source snapshots are append-only. After 20 completed sessions review and pause this USD experiment; continue the GBP experiment. No main changes, deployment, merging or rule tuning.
