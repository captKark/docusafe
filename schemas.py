from datetime import datetime
from pydantic import BaseModel

# Base Schema (Shared properties)
class UserBase(BaseModel):
    name: str
    email: str
    experience_years: int

# Create Schema (Used only for Input)
class UserCreate(UserBase):
    password: str

# Response Schema (Used only for Output)
class UserResponse(UserBase):
    id: int
    status: str

    class Config:
        from_attributes = True # Tells Pydantic to read from ORM models

class Token(BaseModel):
    access_token: str
    token_type: str

# INPUT: What the user sends to create a Document
class DocumentCreate(BaseModel):
    title: str
    content: str

# OUTPUT: What we send back to the user
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    summary: str | None = None # Optional field for summary / Summary can be Null

    class Config:
        from_attributes = True