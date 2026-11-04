from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_demo_and_all_eight_stocks():
    app = AppTest.from_file(APP).run(timeout=20)
    assert not app.exception
    assert len(app.tabs[1].selectbox[0].options) == 8
    assert len(app.tabs[1].dataframe) == 2
    app.tabs[1].selectbox[0].select("POET").run()
    assert not app.exception
    assert "SYNTHETIC" in app.warning[0].value


def test_upload_requires_data_confirmation():
    app = AppTest.from_file(APP).run(timeout=20)
    app.radio[0].set_value("Upload historical CSV").run()
    assert not app.exception
    assert len(app.tabs[1].dataframe) == 0
    assert "Upload" in app.info[0].value


def test_saved_period_and_stock_filters():
    app = AppTest.from_file(APP).run(timeout=20)
    results = app.tabs[0]
    assert results.dataframe[0].value.iloc[0, 0] == 8.68
    results.selectbox[1].select("PLTR").run()
    trades = app.tabs[0].dataframe[1].value
    assert len(trades) == 32 and set(trades.ticker) == {"PLTR"}
    app.tabs[0].selectbox[0].select("2025-03-18").run()
    assert app.tabs[0].dataframe[0].value.iloc[0, 0] == 42.65
    assert len(app.tabs[0].dataframe[1].value) == 7
