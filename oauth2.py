from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import database, models, auth

# this tells FastAPI that the route to get a new token is /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to get the current user based on the JWT token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # Decode the JWT token to get the payload
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        # Decode the token using our secret key and algorithm
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])

        # Extract the user_id from the payload
        user_id: int = payload.get("user_id")

        # If user_id is not found, raise an exception
        if user_id is None:
            raise credentials_exception
    
    # If there's an error decoding the token, raise an exception
    except JWTError:
        raise credentials_exception
    
    # Fetch the user from the database
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # If user is not found, raise an exception
    if user is None:
        raise credentials_exception
    
    return user



