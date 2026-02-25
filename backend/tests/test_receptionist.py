from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_receptionist_endpoint():
    response = client.post(
        "/agent/receptionist",
        json={
            "message": "I want to book appointment",
            "patient_id": "123",
            "patient_info": {"age": 25}
        }
    )

    assert response.status_code == 200
    assert "response" in response.json()