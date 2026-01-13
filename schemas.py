# Moved the UserPayLoad class from the routers/users.py to here, the new file, schemas.py


from pydantic import BaseModel

class UserPayLoad(BaseModel):
    name: str
    experience_years: int