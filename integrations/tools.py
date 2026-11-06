"""Run with python -m integrations.tools --help; optional imports are lazy."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

from engine import WATCHLIST, validate_prices

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path(__file__).with_name("registry.json")


def registry():
    return json.loads(REGISTRY.read_text())


def check_source(tool, source):
    source = Path(source).resolve()
    head = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    if head != registry()[tool]["commit"]:
        raise ValueError(f"{tool}: checkout does not match registry commit")
    dirty = subprocess.check_output(
        ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    ).strip()
    if dirty:
        raise ValueError(f"{tool}: tracked source has local changes")
    return source


def load_prices(path, ticker, as_of=None, candles=False):
    raw = pd.read_csv(path)
    if ticker not in WATCHLIST:
        raise ValueError("Only the eight recorded AI Pie stocks are supported")
    if "ticker" not in raw or not raw.ticker.eq(ticker).all():
        raise ValueError("CSV ticker must match the requested stock")
    prices = validate_prices(raw)
    if as_of is not None:
        cutoff = pd.Timestamp(as_of, tz="UTC")
        prices = prices.loc[prices.index <= cutoff]
    if len(prices) < 3:
        raise ValueError("Insufficient history at cutoff")
    if candles:
        if not {"high", "low"}.issubset(raw.columns):
            raise ValueError("Kronos requires real high/low data; never fabricate it")
        raw.index = pd.to_datetime(raw.date, utc=True)
        for name in ["high", "low", "volume", "amount"]:
            if name in raw:
                prices[name] = pd.to_numeric(
                    raw.loc[prices.index, name], errors="raise"
                )
                if not np.isfinite(prices[name]).all():
                    raise ValueError(f"Invalid {name}")
                if (prices[name] < 0).any():
                    raise ValueError(f"Negative {name}")
        if not (
            (prices.low > 0)
            & (prices.low <= prices[["open", "close"]].min(axis=1))
            & (prices.high >= prices[["open", "close"]].max(axis=1))
        ).all():
            raise ValueError("Inconsistent OHLC candle")
    return prices


def future_sessions(path, last):
    dates = pd.to_datetime(pd.read_csv(path)["date"], utc=True, errors="raise")
    if (
        len(dates) == 0
        or dates.isna().any()
        or dates.duplicated().any()
        or not dates.is_monotonic_increasing
        or not (dates > last).all()
    ):
        raise ValueError("Supply unique increasing exchange sessions after the cutoff")
    return dates.dt.tz_localize(None)


def new_output(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    return path


def write_metadata(out, tool, **extra):
    metadata = {
        "tool": tool,
        "upstream_commit": registry()[tool]["commit"],
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "research_only",
        "eligible_for_forward_ledger": False,
        **extra,
    }
    (out / "metadata.json").write_text(json.dumps(metadata, indent=2))


def export_data(args):
    # Validate the entire batch before creating output, avoiding partial exports.
    inputs = Path(args.inputs)
    frames = {
        ticker: load_prices(inputs / f"{ticker}.csv", ticker) for ticker in WATCHLIST
    }
    reference = frames[next(iter(WATCHLIST))].index
    if any(not frame.index.equals(reference) for frame in frames.values()):
        raise ValueError("All eight stocks must have identical session dates")
    out = new_output(args.output)
    hashes = {}
    for ticker, frame in frames.items():
        hashes[ticker] = hashlib.sha256(
            (inputs / f"{ticker}.csv").read_bytes()
        ).hexdigest()
        frame = frame[["open", "close"]].copy()
        frame.index = frame.index.strftime("%Y-%m-%d")
        if args.tool == "qlib":
            frame = frame.assign(symbol=ticker)
        frame.to_csv(out / f"{ticker}.csv", index_label="date")
    write_metadata(out, args.tool, input_sha256=hashes, fields=["open", "close"])
    if args.tool == "lean":
        print("Copy these CSVs to the LEAN data folder under ai-pie/.")
    else:
        print("Ready for Qlib dump_bin.py with --include_fields open,close.")


def run_qlib(args):
    import qlib
    from qlib.data import D

    qlib.init(provider_uri=str(Path(args.data).resolve()), region="us")
    # Read only historical features. No future-return labels or fitting here.
    frame = D.features(
        list(WATCHLIST),
        ["$close", "Mean($close, 50)", "$close/Ref($close, 1)-1"],
        start_time=args.start,
        end_time=args.end,
        freq="day",
    )
    if frame.empty:
        raise ValueError("No Qlib observations in requested interval")
    out = new_output(args.output)
    frame.to_csv(out / "features.csv")
    write_metadata(out, "qlib", start=args.start, end=args.end)


def run_kronos(args):
    for revision in [args.model_revision, args.tokenizer_revision]:
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Model and tokenizer revisions must be full commit SHAs")
    source = check_source("kronos", args.source)
    prices = load_prices(args.csv, args.ticker, args.as_of, candles=True).tail(512)
    future = future_sessions(args.sessions, prices.index[-1])
    sys.path.insert(0, str(source))
    import torch
    from model import Kronos, KronosTokenizer, KronosPredictor

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    model = Kronos.from_pretrained(args.model, revision=args.model_revision)
    tokenizer = KronosTokenizer.from_pretrained(
        "NeoQuasar/Kronos-Tokenizer-base", revision=args.tokenizer_revision
    )
    predictor = KronosPredictor(model, tokenizer, device=args.device, max_context=512)
    out = new_output(args.output)
    predictions = predictor.predict(
        df=prices.reset_index(drop=True),
        x_timestamp=pd.Series(prices.index.tz_localize(None)),
        y_timestamp=future,
        pred_len=len(future),
        sample_count=5,
        T=1.0,
        top_p=0.9,
    )
    predictions.to_csv(out / "forecast.csv", index_label="date")
    prices.to_csv(out / "input.csv")
    write_metadata(
        out,
        "kronos",
        ticker=args.ticker,
        cutoff=str(prices.index[-1]),
        model=args.model,
        model_revision=args.model_revision,
        tokenizer_revision=args.tokenizer_revision,
        seed=args.seed,
        sample_count=5,
        device=args.device,
        input_sha256=hashlib.sha256(Path(args.csv).read_bytes()).hexdigest(),
        sessions_sha256=hashlib.sha256(Path(args.sessions).read_bytes()).hexdigest(),
        training_overlap="not_verified",
        label="forecast, not a trading signal",
    )


def run_tradingagents(args):
    # Enforce a current-date research report; historical LLM runs may leak future news.
    today = datetime.now(timezone.utc).date().isoformat()
    if args.date != today:
        raise ValueError("TradingAgents is restricted to today's research report")
    source = check_source("tradingagents", args.source)
    sys.path.insert(0, str(source))
    from tradingagents.default_config import DEFAULT_CONFIG
    from tradingagents.graph.trading_graph import TradingAgentsGraph

    out = new_output(args.output)
    config = DEFAULT_CONFIG.copy()
    config.update(
        llm_provider=args.provider,
        deep_think_llm=args.deep_model,
        quick_think_llm=args.quick_model,
        max_debate_rounds=1,
        max_risk_discuss_rounds=1,
        max_tool_rounds=3,
        results_dir=str(out / "reports"),
        data_cache_dir=str(out / "cache"),
        memory_log_path=str(out / "memory.md"),
        checkpoint_enabled=False,
        deep_think_provider=None,
        quick_think_provider=None,
        deep_think_backend_url=None,
        quick_think_backend_url=None,
    )
    state, decision = TradingAgentsGraph(debug=False, config=config).propagate(
        args.ticker, args.date
    )
    (out / "decision.txt").write_text(str(decision))
    (out / "report.json").write_text(json.dumps(state, default=str, indent=2))
    write_metadata(
        out,
        "tradingagents",
        ticker=args.ticker,
        date=args.date,
        provider=args.provider,
        deep_model=args.deep_model,
        quick_model=args.quick_model,
        label="unverified AI research; no automatic trading signal",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    export = commands.add_parser("export")
    export.add_argument("tool", choices=["qlib", "lean"])
    export.add_argument("--inputs", default=str(ROOT / "research" / "inputs"))
    export.add_argument("--output", required=True)
    qlib = commands.add_parser("qlib")
    qlib.add_argument("--source", required=True)
    qlib.add_argument("--data", required=True)
    qlib.add_argument("--start", required=True)
    qlib.add_argument("--end", required=True)
    qlib.add_argument("--output", required=True)
    kronos = commands.add_parser("kronos")
    for flag in [
        "source",
        "csv",
        "as-of",
        "sessions",
        "model-revision",
        "tokenizer-revision",
        "output",
    ]:
        kronos.add_argument("--" + flag, required=True)
    kronos.add_argument("--ticker", required=True, choices=WATCHLIST)
    kronos.add_argument(
        "--model",
        choices=["NeoQuasar/Kronos-small", "NeoQuasar/Kronos-base"],
        default="NeoQuasar/Kronos-small",
    )
    kronos.add_argument("--device", default="cpu")
    kronos.add_argument("--seed", type=int, default=42)
    agent = commands.add_parser("tradingagents")
    for flag in ["source", "provider", "deep-model", "quick-model", "output"]:
        agent.add_argument("--" + flag, required=True)
    agent.add_argument("--ticker", required=True, choices=WATCHLIST)
    agent.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    args = parser.parse_args()
    if args.command == "status":
        print(json.dumps(registry(), indent=2))
    elif args.command == "export":
        export_data(args)
    elif args.command == "qlib":
        source = check_source("qlib", args.source)
        sys.path.insert(0, str(source))
        run_qlib(args)
    elif args.command == "kronos":
        run_kronos(args)
    else:
        run_tradingagents(args)


if __name__ == "__main__":
    main()
