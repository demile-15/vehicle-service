import requests as rq   # send HTTP request
import json             # serialize and deserialize json bodies

BASE_URL = "http://127.0.0.1:8000"  # http://localhost:8000

def test_create_vehicle():
    url = f"{BASE_URL}/vehicle"

    payload = {
        "manufacturer_name": "Toyota",
        "description": "Integration test vehicle",
        "horse_power": 180,
        "model_name": "Camry",
        "model_year": 2022,
        "purchase_price": 27000,
        "fuel_type": "Gas"
    }

    response = rq.post(url, json=payload)

    assert response.status_code == 201

    data = response.json()   
    assert data["manufacturer_name"] == "Toyota"
    assert data["description"] == "Integration test vehicle"
    assert data["horse_power"] == 180
    assert "vin" in data

    # restore db state
    vin = data["vin"]
    url = f"{BASE_URL}/vehicle/{vin}"
    response = rq.delete(url)
    assert response.status_code == 204

def test_invalid_json():
    url = f"{BASE_URL}/vehicle"

    bad_payload = {
        "manufacturer_name": 122334,  # number instead of string
        "description": "Integration test vehicle",
        "horse_power": 180,
        "model_name": "Camry",
        "model_year": 2022,
        "purchase_price": 27000,
        "fuel_type": "Gas"
    }

    response = rq.post(url, json=bad_payload)

    assert response.status_code == 422
    print(response.json())
