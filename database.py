import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DATABASE_URL from environment, fallback to local default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://myuser:password@localhost:5432/bookstore"
)

# Create engine with future=True for SQLAlchemy 2.0 style
engine = create_engine(DATABASE_URL, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for models
Base = declarative_base()

# FastAPI dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
