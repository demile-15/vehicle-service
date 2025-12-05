from sqlalchemy import Column, String, Integer, Float
import uuid 
from database import Base

def generate_vin():
    """
    Function to generate a random identifier
    """
    return uuid.uuid4().hex[:18].upper()

class Vehicle(Base):
    __tablename__ = "vehicles"

    vin = Column(String, primary_key=True, unique=True, index=True, default=generate_vin)
    manufacturer_name = Column(String)
    description = Column(String)
    horse_power = Column(Integer)
    model_name = Column(String)
    model_year = Column(Integer)
    purchase_price = Column(Float)
    fuel_type = Column(String)