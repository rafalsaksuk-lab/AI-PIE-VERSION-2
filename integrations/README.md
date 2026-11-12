# Optional research tools

Research branch only. No brokerage connection, orders, deployment, or changes to either frozen forward experiment.

## Current status

The registry restores dashboard startup and the status command. Its commits were retrieved from the official repositories on 12 November 2026 as candidate revisions, not validated installations. None of the four external tools has a verified execution here. Dependencies in requirements.txt and requirements-dev.txt are for this project, not these external runtimes.

| Tool | Existing support | Still required |
|---|---|---|
| Kronos | Forecast adapter with real OHLC validation and pinned source/model checks | Isolated runtime, verified OHLC data, pinned model/tokenizer weights, actual inference test |
| Qlib | CSV export and historical feature adapter | Isolated runtime, data conversion, feature comparison |
| TradingAgents | Current-date report adapter | Isolated runtime, configured provider, bounded-cost report test |
| LEAN | CSV export only | LEAN runtime and replay algorithm; independent engine comparison |

## Check this project

From the repository root:

```bash
python -m pip install -r requirements-dev.txt
python -m integrations.tools status
python -m integrations.tools --help
python -m pytest -q
```

## External setup sequence

Use a separate environment for each tool. Read the upstream installation instructions at the registry's exact commit before installing dependencies. Clone the corresponding registry URL outside this project, checkout its full commit, and verify a clean tracked working tree. The adapter checks that source pin. Registry pins do not pin transitive dependencies or model weights; record those separately before claiming reproducibility.

Kronos requires real high/low fields, a consistent OHLC adjustment basis, verified exchange dates and full 40-character model/tokenizer revisions. Use the kronos --help command for arguments. Existing open/close-only inputs are insufficient; do not fabricate candles. Forecasts are not trading signals and training overlap remains unverified.

Qlib export writes open/close CSVs only; convert with the pinned upstream dump_bin.py before using the feature adapter. TradingAgents only accepts today's date to avoid historical news leakage; provider credentials and cost limits must be configured separately, never committed. LEAN export does not install LEAN or supply an executable LEAN algorithm.

Keep outputs outside the forward ledgers. No external output may change current paper signals. Installation, smoke testing and out-of-sample evaluation are separate remaining milestones.
