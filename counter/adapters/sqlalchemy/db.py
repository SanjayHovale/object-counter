from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from counter.adapters.sqlalchemy.models import Base

# 1. Replace <password> with your actual PostgreSQL password
DATABASE_URL = "postgresql+psycopg2://postgres:Sanjay%40144@localhost/object_counter"

# 2. Create a database engine
engine = create_engine(DATABASE_URL)

# 3. Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create all tables in the database (if they don’t already exist)
Base.metadata.create_all(bind=engine)
