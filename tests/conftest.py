import pytest
import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event # <-- Added event for SQLite PRAGMA
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# 1. Use an In-Memory SQLite Database (Vanishes after tests)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# We verify if the database is SQLite, then we inject the "now" function
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # This creates a function named "now" inside SQLite that returns the current time
    dbapi_connection.create_function("now", 0, 
        lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Override the real database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Create the Test Client fixture
@pytest.fixture(scope="function") # Scope="function" means we reset for every test function
def client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Drop tables (Cleanup)
    Base.metadata.drop_all(bind=engine)