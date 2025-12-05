from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_vehicle():
    data = {
        "vin": "TESTVIN123",
        "manufacturer_name": "Honda",
        "description": "Test car",
        "horse_power": 150,
        "model_name": "Civic",
        "model_year": 2021,
        "purchase_price": 22000,
        "fuel_type": "Gas"
    }

    response = client.post("/vehicle", json=data)
    assert response.status_code == 201

    body = response.json()
    assert body["vin"] == "TESTVIN123"
