# Vehicle Database Web Service
This project implements a RESTful web service that provides CRUD-style API access to stored vehicle records.
It was built using `FastAPI`, `SQLAlchemy`, and `SQLite`, and includes basic automated tests using `pytest`.

## Features
| Endpoint         | Description           | Method | Status         |
| ---------------- | --------------------- | ------ | -------------- |
| `/vehicle`       | Get all vehicles      | GET    | 200 OK         |
| `/vehicle`       | Create a vehicle      | POST   | 201 Created    |
| `/vehicle/{vin}` | Get vehicle by VIN    | GET    | 200 OK         |
| `/vehicle/{vin}` | Update vehicle by VIN | PUT    | 200 OK         |
| `/vehicle/{vin}` | Delete vehicle by VIN | DELETE | 204 No Content |

Additional behaviors:
- VIN is used as the primary identifier (case-insensitive)
- Validates JSON payload using Pydantic models
- Returns 400/422 on malformed input
- Returns 404 for missing VIN
- Tested via pytest

## Tech Stack
- FastAPI: web framework for building APIs
- SQLAlchemy: ORM and database layer
- SQLite: simple local persistent DB
- pytest: automated test runner
- Uvicorn: ASGI server to run FastAPI

## Running the App
**1. Install dependencies**
```
pip install -r requirements.txt
```

**2. Start the server**
```
uvicorn main:app --reload
```

**3. Open interactive API docs:**
```
http://localhost:8000/docs
```

From here, you can test all endpoints via Swagger UI.

## Running Tests
Run `pytest -q` to run unit tests.


## Future Improvements
Given more time, I'd implement the following:
- Independent in-memory DB for `pytest` runs.
- More extensive test coverage (+ failure case tests).
- Optional AWS deployment.