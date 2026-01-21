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