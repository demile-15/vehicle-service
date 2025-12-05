import requests as rq   # send HTTP request
import json             # serialize and deserialize json bodies

BASE_URL = "http://127.0.0.1:8000"  # http://localhost:8000

def restore_db_state(vins: list[str]):
    for vin in vins:
        response = rq.delete(f"{BASE_URL}/vehicle/{vin}")
        assert response.status_code == 204

def test_create_vehicle():
    url = f"{BASE_URL}/vehicle"

    payload = {
        "manufacturer_name": "Hyundai",
        "description": "Sedan",
        "horse_power": 200,
        "model_name": "Tucson",
        "model_year": 2018,
        "purchase_price": 30000,
        "fuel_type": "Gas"
    }

    response = rq.post(url, json=payload)
    assert response.status_code == 201

    data = response.json()   
    assert data["manufacturer_name"] == "Hyundai"
    assert data["description"] == "Sedan"
    assert data["horse_power"] == 200
    assert "vin" in data

    restore_db_state([data["vin"]])


def test_get_vehicle_by_vin():
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
    assert "vin" in data
    vin = data["vin"]

    # get a vehicle by its VIN
    url = f"{BASE_URL}/vehicle/{vin}"
    response = rq.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "Camry"

    # restore db state
    restore_db_state([data["vin"]])


def test_update_vehicle():
    url = f"{BASE_URL}/vehicle"
    payload = {
        "manufacturer_name": "Hyundai",
        "description": "Sedan",
        "horse_power": 200,
        "model_name": "Tucson",
        "model_year": 2018,
        "purchase_price": 30000,
        "fuel_type": "Gas"
    }
    response = rq.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    vin = data["vin"]
    
    assert data["manufacturer_name"] == "Hyundai"
    assert data["model_year"] == 2018

    # update a vehicle by its VIN
    updated_payload = {
        "manufacturer_name": "Hyundai",
        "description": "Sedan",
        "horse_power": 200,
        "model_name": "Tucson",
        "model_year": 2020,
        "purchase_price": 30000,
        "fuel_type": "Gas"
    }
    url = f"{BASE_URL}/vehicle/{vin}"
    response = rq.put(url, json=updated_payload)

    assert response.status_code == 200
    data = response.json()

    assert data["manufacturer_name"] == "Hyundai"
    assert data["model_year"] == 2020

    # restore db state
    restore_db_state([vin])

def test_delete_vehicle():
    url = f"{BASE_URL}/vehicle"
    payload = {
        "manufacturer_name": "Hyundai",
        "description": "Sedan",
        "horse_power": 200,
        "model_name": "Tucson",
        "model_year": 2018,
        "purchase_price": 30000,
        "fuel_type": "Gas"
    }
    response = rq.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    vin = data["vin"]

    url = f"{BASE_URL}/vehicle/{vin}"
    response = rq.delete(url)
    assert response.status_code == 204

    # cannot retrieve deleted vehicle
    response = rq.get(url)
    assert response.status_code == 404

    # cannot delete same object twice (ID not found)
    response = rq.delete(url)
    assert response.status_code == 404
