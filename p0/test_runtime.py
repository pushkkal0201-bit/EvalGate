from fastapi.testclient import TestClient

from main import app
from runtime import MAX_BODY_BYTES


def test_authentication_and_metrics(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-only-key")
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.post("/v1/regression/paired", json={'baseline': [0, 0], 'candidate': [1, 1], 'samples': 100}).status_code == 401
        response = client.post(
            "/v1/regression/paired", json={'baseline': [0, 0], 'candidate': [1, 1], 'samples': 100}, headers={"X-API-Key": "test-only-key"}
        )
        assert response.status_code == 200
        assert response.json()["lower"] == 1
        assert 'route="/v1/regression/paired",status="200"' in client.get("/metrics/").text


def test_streamed_body_limit(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    with TestClient(app) as client:
        response = client.post("/v1/regression/paired", content=b" " * (MAX_BODY_BYTES + 1))
        assert response.status_code == 413
