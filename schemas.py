from pydantic import BaseModel, Field

class VehicleBase(BaseModel):
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int # = Field(..., ge=1886)      # first car invented
    purchase_price: float
    fuel_type: str

class VehicleCreate(VehicleBase):
    vin: str

class VehicleResponse(VehicleBase):
    vin: str

    class Config:
        orm_mode = True   # allows DB object for JSON conversion