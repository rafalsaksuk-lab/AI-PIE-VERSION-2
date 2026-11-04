import pandas as pd
import pytest
from engine import validate_prices, simulate


def frame():
    return pd.DataFrame(
        {
            "date": pd.bdate_range("2026-01-01", periods=6),
            "open": [10, 12, 14, 6, 7, 8],
            "close": [10, 12, 6, 7, 8, 9],
        }
    )


@pytest.mark.parametrize("value", [0, -1, float("nan"), float("inf")])
def test_bad_prices(value):
    data = frame()
    data["open"] = data["open"].astype(float)
    data.loc[1, "open"] = value
    with pytest.raises(ValueError):
        validate_prices(data)


def test_missing_columns():
    with pytest.raises(ValueError):
        validate_prices(frame().drop(columns="open"))


def test_missing_date():
    data = frame()
    data.loc[1, "date"] = pd.NaT
    with pytest.raises(ValueError):
        validate_prices(data)


def test_reverse_dates():
    with pytest.raises(ValueError):
        validate_prices(frame().iloc[::-1])


def test_short_data():
    with pytest.raises(ValueError):
        validate_prices(frame().iloc[:2])


@pytest.mark.parametrize(
    "window,cost,initial",
    [
        (1, 10, 1000),
        (100, 10, 1000),
        (2, -1, 1000),
        (2, 501, 1000),
        (2, 10, 0),
        (2, 10, float("inf")),
    ],
)
def test_invalid_settings(window, cost, initial):
    with pytest.raises(ValueError):
        simulate(validate_prices(frame()), window, cost, initial)


def test_sell_on_next_available_session_and_exit_fee():
    prices = validate_prices(frame())
    equity, trades = simulate(prices, 2, 100, 1000)
    assert trades.iloc[0]["side"] == "BUY"
    assert trades.iloc[0]["price"] == 14
    assert trades.iloc[1]["side"] == "SELL"
    assert trades.iloc[1]["price"] == 6
    expected = 1000 / (14 * 1.01) * 6 * 0.99
    assert equity.iloc[1]["Strategy"] == pytest.approx(expected)


def test_prefix_invariance():
    prices = validate_prices(frame())
    full, trades = simulate(prices, 2)
    prefix, prefix_trades = simulate(prices.iloc[:4], 2)
    pd.testing.assert_frame_equal(full.iloc[:2], prefix)
    pd.testing.assert_frame_equal(
        trades[trades.date <= prices.index[3]].reset_index(drop=True), prefix_trades
    )
