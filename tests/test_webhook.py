from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_webhook_order_status():
    response = client.post("/webhook", json={
        "user_id": "test_user",
        "message": "What is the status of my order?"
    })
    assert response.status_code == 200
    assert "response" in response.json()
