import socket
import uuid

import pytest
from fastapi.testclient import TestClient

from config import settings
from db.seed import DEMO_EMAIL, DEMO_PASSWORD


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Fail any test that tries to open an outbound connection."""

    def guard(*args, **kwargs):
        raise RuntimeError("Tests must not make network calls")

    monkeypatch.setattr(socket, "create_connection", guard)
    monkeypatch.setattr(socket.socket, "connect", guard)


@pytest.fixture
def client(tmp_path, monkeypatch):
    """The API running in-process against a throwaway database."""
    monkeypatch.setattr(settings, "database_path", str(tmp_path / "test.db"))
    from main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def anon_headers():
    return {"X-Basket-Id": str(uuid.uuid4())}


def login(client, email=DEMO_EMAIL, password=DEMO_PASSWORD, headers=None):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
        headers=headers or {},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def demo_headers(client):
    return login(client)
