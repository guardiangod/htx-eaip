from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_search_empty_query_returns_400():
    r = client.get("/search")
    assert r.status_code == 400
