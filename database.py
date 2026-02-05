from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os  # <--- NEW: We need this to read variables

# 1. Database Connection URL
# Logic: Try to get the variable from the Environment (Render). 
# If it's missing (Local laptop), use the hardcoded default.

db_user = os.environ.get("DATABASE_USERNAME", "user")
db_password = os.environ.get("DATABASE_PASSWORD", "password")
db_host = os.environ.get("DATABASE_HOSTNAME", "localhost")
db_port = os.environ.get("DATABASE_PORT", "5432")
db_name = os.environ.get("DATABASE_NAME", "docusafe_db")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# 2. Database Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# 3. Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Declarative Base
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()