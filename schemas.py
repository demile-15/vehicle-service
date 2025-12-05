from pydantic import BaseModel, ConfigDict

class VehicleBase(BaseModel):
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: float
    fuel_type: str

class VehicleCreate(VehicleBase):
    vin: str

class VehicleResponse(VehicleBase):
    vin: str

    # allow SQLAlchemy objects to be converted to JSON responses
    model_config = ConfigDict(from_attributes=True)