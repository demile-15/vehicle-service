from pydantic import BaseModel, ConfigDict

class VehicleRequest(BaseModel):
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str

class VehicleUpdate(VehicleRequest):
    vin: str

class VehicleResponse(VehicleRequest):
    vin: str

    # allow SQLAlchemy objects to be converted to JSON responses
    model_config = ConfigDict(from_attributes=True)