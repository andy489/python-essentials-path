import os
from unittest.mock import Mock

import storage
from storage import store_alert, fetch_alerts


def test_store_alert(tmp_path):
    clash = "Bob with number 1234"
    store_alert(clash, tmp_path)
    with open(os.path.join(tmp_path, "alert_log.txt"), "r") as f:
        contents = f.read()
        assert contents == """Bob with number 1234\n"""


def test_fetch_alerts(tmp_path, monkeypatch):
    with open(os.path.join(tmp_path, "alert_log.txt"), "w") as f:
        f.write("""new alert: clash with Bob with number 1234\n""")
    stub_count_alerts = Mock(return_value={"alert": 2})
    monkeypatch.setattr(storage, "count_alerts", stub_count_alerts)

    alerts = fetch_alerts(tmp_path)

    assert alerts == {"alert": 2}


def test_fetch_alerts_missing_file(tmp_path):
    # No alerts file is present
    alerts = fetch_alerts(tmp_path)

    assert alerts == {}
