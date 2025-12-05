from sqlalchemy import Column, String, Integer, Float
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, unique=True, index=True)
    manufacturer_name = Column(String)
    description = Column(String)
    horse_power = Column(Integer)
    model_name = Column(String)
    model_year = Column(Integer)
    purchase_price = Column(Float)
    fuel_type = Column(String)