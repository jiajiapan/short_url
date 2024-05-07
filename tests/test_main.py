from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.json().get("message") == "this is short url website."
    assert res.status_code == 200


def test_shorten_url():
    res = client.post("/api/v1/shorturl", json={"long_url": "www5"})
    assert res.json().get("short_url") == "b0df12f"
    assert res.status_code == 201


def test_redirect_url_exists():
    res = client.post("/api/v1/longurl", json={"short_url": "b0df12f"})
    assert res.json().get("long_url") == "www5"
    assert res.status_code == 200


def test_redirect_url_does_not_exist():
    res = client.post("/api/v1/longurl", json={"short_url": "1234567"})
    assert res.status_code == 404
