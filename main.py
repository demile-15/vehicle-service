from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Vehicle
from schemas import VehicleCreate, VehicleResponse

app = FastAPI(title="Vehicle Service")

def get_db():
    """
    Read all vehicles
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

    Response Status: "200 OK"
    Request Entity: JSON-formatted representation of vehicles
    Response Entity: JSON-formatted representation of all records in "Vehicle" table

    
    :param db: the database
    :type db: Session
    """
    return db.query(Vehicle).all()
