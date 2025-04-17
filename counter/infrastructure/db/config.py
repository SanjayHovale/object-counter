from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Adjust this URL for MySQL if needed
DATABASE_URL = "postgresql://username:password@localhost:5432/object_counter"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
