import unittest
import pandas as pd
from engine import validate_prices, simulate, metrics


class EngineTests(unittest.TestCase):
    def prices(self):
        return validate_prices(
            pd.DataFrame(
                {
                    "date": pd.date_range("2020-01-01", periods=8),
                    "open": [10, 11, 12, 13, 14, 15, 16, 17],
                    "close": [10, 11, 12, 13, 14, 15, 16, 17],
                }
            )
        )

    def test_no_future_information(self):
        p = self.prices()
        first, t1 = simulate(p, 2)
        p.iloc[-1, p.columns.get_loc("close")] = 1
        second, t2 = simulate(p, 2)
        pd.testing.assert_frame_equal(first.iloc[:-1], second.iloc[:-1])
        pd.testing.assert_frame_equal(t1, t2)

    def test_next_open_and_cost(self):
        p = self.prices()
        eq, trades = simulate(p, 2, 100, 1000)
        self.assertEqual(trades.iloc[0]["price"], 12)
        self.assertAlmostEqual(eq.iloc[0]["Strategy"], 1000 / 1.01)
        self.assertAlmostEqual(eq.iloc[0]["Buy and hold"], 1000 / 1.01)

    def test_future_open_change_does_not_change_earlier_fills(self):
        p = self.prices()
        a, _ = simulate(p, 2)
        p.iloc[-1, p.columns.get_loc("open")] = 1000
        b, _ = simulate(p, 2)
        pd.testing.assert_frame_equal(a.iloc[:-1], b.iloc[:-1])

    def test_duplicate_dates_rejected(self):
        p = self.prices().reset_index()
        p.loc[1, "date"] = p.loc[0, "date"]
        with self.assertRaises(ValueError):
            validate_prices(p)

    def test_drawdown_includes_starting_capital(self):
        self.assertAlmostEqual(
            metrics(pd.Series([900, 950]), 1000)["Max drawdown (%)"], -10
        )

    def test_flat_market_stays_in_cash(self):
        p = self.prices()
        p.loc[:, ["open", "close"]] = 10
        eq, trades = simulate(p, 2)
        self.assertTrue(trades.empty)
        self.assertTrue((eq.Strategy == 1000).all())


if __name__ == "__main__":
    unittest.main()
