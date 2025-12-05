import requests as rq   # send HTTP request
import json             # serialize and deserialize json bodies

BASE_URL = "http://127.0.0.1:8000"  # http://localhost:8000

def test_create_vehicle():
    url = f"{BASE_URL}/vehicle"

    json_body = {
        "manufacturer_name": "Toyota",
        "description": "Integration test vehicle",
        "horse_power": 180,
        "model_name": "Camry",
        "model_year": 2022,
        "purchase_price": 27000,
        "fuel_type": "Gas"
    }

    response = rq.post(url, json=json_body)

    assert response.status_code == 201
    data = response.json()   
    assert data["manufacturer_name"] == "Toyota"
    assert "vin" in data
    vin = data["vin"]

    # restore db state
    url = f"{BASE_URL}/vehicle/{vin}"

    response = rq.delete(url)
    assert response.status_code == 204
    
    response = rq.get(url)
    assert response.status_code == 404


# def test_get_vehicle_by_vin():
#     url = f"{BASE_URL}/vehicle/VINTEST999"

#     response = rq.get(url)

#     assert response.status_code == 200
#     data = response.json()
#     assert data["description"] == "Integration test vehicle"


# def test_delete_vehicle():
#     url = f"{BASE_URL}/vehicle/VINTEST999"

#     response = rq.delete(url)

#     assert response.status_code == 204
    
#     response = rq.get(url)
#     assert response.status_code == 404


# def test_invalid_payload_returns_400():
#     url = f"{BASE_URL}/vehicle"

#     # missing quotes around keys → invalid JSON
#     bad_payload = "{vin:123}"  

#     response = rq.post(
#         url,
#         data=bad_payload,       # send raw instead of json=
#         headers={"Content-Type": "application/json"}
#     )

#     assert response.status_code == 400
#     assert "Invalid JSON" in response.text