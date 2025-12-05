from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Vehicle
from schemas import VehicleCreate, VehicleResponse

app = FastAPI(title="Vehicle Service")

def get_db():
    """
    Gives FastAPI a database session to work with
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/vehicle", response_model=list[VehicleResponse])
def get_all_vehicles(db: Session = Depends(get_db)):
    """
    GET/vehicle 

    - Response Status: "200 OK"
    - Request Entity: JSON-formatted representation of vehicles
    - Response Entity: JSON-formatted representation of all records in "Vehicle" table
    
    :param db: the database
    :type db: Session
    """
    return db.query(Vehicle).all()

@app.post("/vehicle", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    POST/vehicle 

    - Response Status: "201 Created"
    - Request Entity: JSON-formatted representation of a unique vehicle
    - Response Entity: JSON-formatted representation of the new vehicle, including its
    unique identifier
    - Side Effects: System assigns a unique identifier and inserts a record into the `Vehicle` table

    :param db: the database
    :type db: Session
    """
    # enforce VIN uniqueness (case-insensitive)
    existing = db.query(Vehicle).filter(Vehicle.vin.ilike(vehicle.vin)).first()
    if existing:
        raise HTTPException(status_code=422, detail="VIN already exists")

    new_vehicle = Vehicle(**vehicle.dict())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)  # gets updated version from DB
    return new_vehicle

