from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./vehicles.db"  # use sqlite

# establish connectivity to a database
# sqlite only allows DB access for a single thread, but FastAPI has multithreading 
# to handle requests -> need different parts of the app to talk to SQLite safely.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  


# create a temporary session to connect to the database
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# create a base class for our data model for sqlalchemy to build tables
Base = declarative_base()