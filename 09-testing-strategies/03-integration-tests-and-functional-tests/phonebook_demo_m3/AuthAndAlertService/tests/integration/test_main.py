from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient

import main
from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


def test_authenticate(client):
    response = client.get("/authenticate")
    assert response.status_code == 200


def test_alert(client, monkeypatch):
    alert = {'size': 3,
             'new_entry': 'Ted cannot be added with number 1234',
             'clash': 'Bob with number 1234'
             }
    spy_storage = Mock()
    monkeypatch.setattr(main, "store_alert", spy_storage)

    response = client.put("/alert", json=alert)

    assert response.status_code == 200
    spy_storage.assert_called_with(
        'Bob with number 1234'
    )


def test_clash_frequencies(client, monkeypatch):
    clash_data = {'Bob with number 1234': 2}
    fetch_alerts = Mock(return_value=clash_data)
    monkeypatch.setattr(main, "fetch_alerts", fetch_alerts)

    response = client.get("/clash_frequencies")

    assert response.status_code == 200
    assert response.json() == {'entries': {'Bob with number 1234': 2}}
