from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from json import JSONDecodeError
from contextlib import asynccontextmanager

from database import SessionLocal
from orm_model import Vehicle
from validation import VehicleRequest, VehicleResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A startup hook that creates "vehicles.db" file on boot.
    """
    from database import engine
    from orm_model import Base
    Base.metadata.create_all(bind=engine)
    yield  # separates "startup" from "shutdown".

app = FastAPI(title="Vehicle Service", lifespan=lifespan)

def get_db():
    """
    Gives FastAPI a database session to work with
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# decorator that attaches a function to a route/url and method
# here, attach get_all_vehicles to GET http://localhost:8000/vehicle
@app.get("/vehicle", response_model=list[VehicleResponse]) # default "200 OK"
def get_all_vehicles(db: Session = Depends(get_db)): 
    """
    Retrieve all vehicles stored in the database.

    Returns:
        List[VehicleResponse]: A list of all vehicle records in JSON format.
    """
    return db.query(Vehicle).all()


@app.post("/vehicle", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleRequest, db: Session = Depends(get_db)):
    """
    Create and assign a unique identifier for a new vehicle entry in the database.

    Args:
        vehicle (VehicleBase): JSON body containing vehicle details.

    Returns:
        VehicleResponse: The newly created vehicle record.
    """
    while True:
        try:
            new_vehicle = Vehicle(**vehicle.model_dump())
            db.add(new_vehicle)
            db.commit()
            db.refresh(new_vehicle)  # refresh to the generated VIN
            return new_vehicle
        except IntegrityError:       # retry in case generated VIN is a duplicate
            db.rollback()
            continue


@app.get("/vehicle/{vin}", response_model=VehicleResponse)
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
def update_vehicle(vin: str, vehicle: VehicleRequest, db: Session = Depends(get_db)):
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
    

# invalid JSON format
@app.exception_handler(JSONDecodeError)
async def json_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"error": "Invalid JSON payload"}
    )


# valid JSON but invalid fields
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": exc.errors()}
    )
