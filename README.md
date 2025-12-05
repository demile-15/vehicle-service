# Vehicle Database Web Service

Step 1: Create database and table model

- `database.py`: Create a database connection using SQLAlchemy's create_engine(). This returns an Engine object that establishes connection to a database.

- `models.py`: Define the Vehicle table

+ Make a class Vehicle
+ Run
`
python3
>>> from database import Base, engine
>>> from models import Vehicle
>>> Base.metadata.create_all(engine)
`

Step 2: Create request/response validation models `schemas.py`
The validation models ensure JSON input is valid and help return 400/422 errors automatically.

Step 3: Build API Endpoints
- Start a FastAPI server
- Implement endpoints: GET/vehicle, 

# API Endpoints
### GET/vehicle

### GET/vehicle/{vin}