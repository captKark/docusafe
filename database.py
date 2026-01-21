from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Database Connection URL
# CHANGE 'YOUR_PASSWORD' to the password you set for the postgres user
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5433/docusafe_db"
# 2. Database Engine
# This handles the actual communication to the DB
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# 3. Session Factory
# This is what we use to create a session (a temporary workspace) to talk to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative Base
# This is the base class for all your DB models/tables
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()