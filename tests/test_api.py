
from fastapi.testclient import TestClient

import app.main as main_module

client = TestClient(main_module.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_answer(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "ask_support",
        lambda question: "Standard shipping takes 3–7 business days.",
    )

    response = client.post(
        "/chat",
        json={"question": "How long does shipping take?"},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "3–7 business days" in response.json()["answer"]


def test_chat_rejects_empty_question():
    response = client.post("/chat", json={"question": ""})

    assert response.status_code == 422


def test_chat_rejects_missing_question():
    response = client.post("/chat", json={})

    assert response.status_code == 422


def test_chat_handles_agent_error(monkeypatch):
    def fail_agent(question):
        raise RuntimeError("Simulated failure")

    monkeypatch.setattr(main_module, "ask_support", fail_agent)

    response = client.post(
        "/chat",
        json={"question": "Check my order"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "The support agent could not process your request."
    )
