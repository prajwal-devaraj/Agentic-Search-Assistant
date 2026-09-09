from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_framework():
    response = client.get("/v1/framework")
    assert response.status_code == 200
    assert response.json()["name"] == "PRAJNA"
    assert len(response.json()["steps"]) == 6


def test_search_demo():
    response = client.post("/v1/search", json={"query": "agentic search", "mode": "deep"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"]
    assert len(body["sources"]) >= 2
    assert body["trust"]["score"] >= 0
    assert [step["name"] for step in body["trace"]] == [
        "Plan", "Retrieve", "Assess", "Join", "Navigate", "Answer"
    ]
