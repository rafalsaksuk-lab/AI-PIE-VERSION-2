from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_demo_and_all_eight_stocks():
    app = AppTest.from_file(APP).run(timeout=20)
    assert not app.exception
    assert len(app.selectbox[0].options) == 8
    assert len(app.dataframe) == 2
    app.selectbox[0].select("POET").run()
    assert not app.exception
    assert "SYNTHETIC" in app.warning[0].value


def test_upload_requires_data_confirmation():
    app = AppTest.from_file(APP).run(timeout=20)
    app.radio[0].set_value("Upload historical CSV").run()
    assert not app.exception
    assert len(app.dataframe) == 0
    assert "Upload" in app.info[0].value
