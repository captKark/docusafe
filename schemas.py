from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# --------------- USER SCHEMAS --------------- #

# Base Schema (Shared properties)
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50) # Name is required, must be between 1 and 50 characters
    email: EmailStr # Validates that the input is a proper email format
    experience_years: int = Field(..., ge=0, le=50) # Constraints: Must be between 0 and 50 years of experience

# Create Schema (Used only for Input)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6) # Password is required, must be at least 6 characters long
 
# Response Schema (Used only for Output)
class UserResponse(UserBase):
    id: int
    status: str

    model_config =ConfigDict(from_attributes=True) # Tells Pydantic to read data from ORM models (SQLAlchemy)


# --------------- AUTH SCHEMAS --------------- #

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]=None # We can have an empty token, so we set it to Optional 


# --------------- DOCUMENT SCHEMAS --------------- #

# INPUT: What the user sends to create a Document
class DocumentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)  # Title is required, and not too long
    content: str = Field(..., min_length=1)  # Content is required, must not be empty

# OUTPUT: What we send back to the user
class DocumentResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    owner_id: int
    summary: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True) # Tells Pydantic to read data from ORM models (SQLAlchemy)
    # tells pydantic to look for attributes on an object (like a SQLAlchemy model) rather than only expecting a dict.