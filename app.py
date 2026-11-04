import pandas as pd
import streamlit as st
from engine import WATCHLIST, validate_prices, simulate, metrics
from pathlib import Path

st.set_page_config(page_title="AI PIE VERSION 2", layout="wide")
st.title("AI PIE VERSION 2")
st.caption("AI Growth stocks • Research and simulation only")
with st.sidebar:
    st.header("Experiment")
    symbol = st.selectbox(
        "AI Growth Pie — last recorded list",
        list(WATCHLIST),
        format_func=lambda ticker: f"{ticker} — {WATCHLIST[ticker]}",
    )
    st.caption(
        "Last recorded eight-stock list; current holdings and weights are unverified. Selection labels your CSV; it does not download prices."
    )
    source = st.radio(
        "Price source", ["Synthetic demonstration", "Upload historical CSV"]
    )
    initial = st.number_input(
        "Starting capital (file currency)", min_value=100.0, value=1000.0
    )
    window = st.number_input(
        "Moving-average sessions", min_value=2, max_value=250, value=50
    )
    costs = st.number_input(
        "Cost per buy/sell (basis points)", min_value=0, max_value=500, value=10
    )
    confirmed = False
    if source == "Upload historical CSV":
        upload = st.file_uploader("date, open, close", type="csv")
        confirmed = st.checkbox(
            "I confirm these are stock prices, with open and close consistently adjusted for splits and dividends."
        )
    else:
        upload = None

if source == "Synthetic demonstration":
    st.warning(
        "SYNTHETIC DATA — these are invented prices, unrelated to the selected company. Results are a software demonstration."
    )
    frame = pd.read_csv(Path(__file__).parent / "data" / "synthetic.csv")
else:
    if upload is None or not confirmed:
        st.info(
            "Upload a daily stock price file and confirm its adjustment basis to begin."
        )
        st.stop()
    frame = pd.read_csv(upload)
    st.info(
        "Uploaded data: provider accuracy, missing sessions and adjustment history are not independently verified."
    )
try:
    prices = validate_prices(frame)
    equity, trades = simulate(prices, int(window), costs, initial)
except (ValueError, TypeError, KeyError) as exc:
    st.error(str(exc))
    st.stop()
st.subheader("Trend strategy versus buy-and-hold")
st.write(
    "Above the moving average at the previous close: hold the asset. Otherwise: cash. Trades execute at the next supplied session open. Both approaches start after the same warm-up period."
)
st.caption(
    f"{equity.index[0].date()} to {equity.index[-1].date()} • {len(equity)} evaluated sessions • Costs apply to entry and exit • End positions marked to market"
)
st.line_chart(equity)
st.dataframe(
    pd.DataFrame({name: metrics(equity[name], initial) for name in equity}).T.round(2)
)
st.subheader("Simulated trades")
st.dataframe(trades)
st.download_button(
    "Download comparison CSV", equity.to_csv(), "comparison.csv", "text/csv"
)
st.download_button(
    "Download simulated trades",
    trades.to_csv(index=False),
    "simulated-trades.csv",
    "text/csv",
)
with st.expander("Assumptions and limits"):
    st.write(
        "Single asset, fractional shares, no leverage or shorting. Cash earns zero. Costs approximate fees, spread and slippage as a proportional charge. No taxes, FX conversion, liquidity limits or market-impact model. No forced sale at the end. Missing sessions are not filled. Use matching currencies and verify data before interpretation. This is an in-sample exploration, not an untouched out-of-sample test."
    )
