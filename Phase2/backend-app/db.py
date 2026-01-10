"""
Database connection and session management using SQLModel
"""
from sqlmodel import create_engine, Session
from typing import Generator
from config import settings
import os

# Create database engine
connection_string = settings.database_url
engine = create_engine(connection_string, echo=False)

def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

# Function to create tables (to be called during app startup)
def create_db_and_tables():
    """Create database tables if they don't exist"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)