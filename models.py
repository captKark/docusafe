# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False) # <--- MUST BE HERE
    password = Column(String, nullable=False)           # <--- MUST BE HERE
    experience_years = Column(Integer)
    status = Column(String, default="Intern")