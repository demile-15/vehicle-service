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

def test_update_vehicle():
    data = {
        "vin": "TESTVIN123",
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horse_power": 155,
        "model_name": "Civic",
        "model_year": 2022,
        "purchase_price": 20000,
        "fuel_type": "Gas"
    }
    response = client.put("/vehicle/TESTVIN123", json=data)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated description"


def test_delete_vehicle():
    response = client.delete("/vehicle/TESTVIN123")
    assert response.status_code == 204

    response = client.get("/vehicle/TESTVIN123")
    assert response.status_code == 404

