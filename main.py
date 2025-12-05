from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Vehicle
from schemas import VehicleCreate, VehicleResponse

# create table Vehicle on startup if it didn't exist
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Service")

@app.on_event("startup")
def startup():
    from database import engine
    from models import Base
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Gives FastAPI a database session to work with
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/vehicle", response_model=list[VehicleResponse]) # default "200 OK"
def get_all_vehicles(db: Session = Depends(get_db)): 
    """
    Retrieve all vehicles stored in the database.

    Returns:
        List[VehicleResponse]: A list of all vehicle records in JSON format.
    """
    return db.query(Vehicle).all()


@app.post("/vehicle", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle entry in the database.

    Args:
        vehicle (VehicleCreate): JSON body containing vehicle details.

    Returns:
        VehicleResponse: The newly created vehicle record.

    Raises:
        HTTPException 422: If VIN already exists in the database.
    """
    # enforce VIN uniqueness (case-insensitive)
    existing = db.query(Vehicle).filter(Vehicle.vin.ilike(vehicle.vin)).first()
    if existing:
        raise HTTPException(status_code=422, detail="VIN already exists")

    new_vehicle = Vehicle(**vehicle.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)  # gets updated version from DB
    return new_vehicle


@app.get("/vehicle{vin}", response_model=VehicleResponse)
def get_vehicle(vin: str, db: Session = Depends(get_db)):
    """
    Retrieve a single vehicle by VIN.

    Args:
        vin (str): The VIN of the vehicle to fetch.

    Returns:
        VehicleResponse: The matching vehicle in JSON format.

    Raises:
        HTTPException 404: If no vehicle with the given VIN exists.
    """
    # search for a case-insensitive match in Vehicle DB
    vehicle = db.query(Vehicle).filter(Vehicle.vin.ilike(vin)).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@app.put("/vehicle/{vin}", response_model=VehicleResponse)
def update_vehicle(vin: str, vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """
    Update an existing vehicle by VIN.

    Args:
        vin (str): VIN of the vehicle to update.
        vehicle (VehicleCreate): Updated vehicle fields from request body.

    Returns:
        VehicleResponse: Updated vehicle data.

    Raises:
        HTTPException 404: If vehicle does not exist.
    """
    # find vehicle by VIN (case-insensitive)
    existing_vehicle = db.query(Vehicle).filter(Vehicle.vin.ilike(vin)).first()
    if not existing_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # update fields:
    for key, value in vehicle.model_dump().items():
        setattr(existing_vehicle, key, value)
    db.commit()
    db.refresh(existing_vehicle)
    return existing_vehicle

@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    """
    Delete a single vehicle by VIN.

    Args:
        vin (str): The VIN of the vehicle to fetch.

    Returns:
        None (204 No Content on success)

    Raises:
        HTTPException 204: If no vehicle with the given VIN exists.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.vin.ilike(vin)).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    db.delete(vehicle)
    db.commit()
    return