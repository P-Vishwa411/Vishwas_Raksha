import os
import sys

# Get the project root directory
current_file = os.path.abspath(__file__)
database_dir = os.path.dirname(current_file)
backend_dir = os.path.dirname(database_dir)
project_root = os.path.dirname(backend_dir)

# Add project root to sys.path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    history = Column(JSON) # Store visit history
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String)
    agent_id = Column(String)
    scheduled_time = Column(DateTime)
    status = Column(String, default="pending") # pending, confirmed, cancelled
    needs_review = Column(Boolean, default=False)

# Database Setup (SQLite for demo, PostgreSQL ready)
DATABASE_URL = "sqlite:///./clinic.db"
# For PostgreSQL: "postgresql://user:password@localhost/hms"

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
