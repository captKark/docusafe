from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import models, schemas, utils, auth

# Create the router for authentication 
router = APIRouter(
    tags=["Authentication"]
)
# Login Endpoint
@router.post("/login", response_model=schemas.Token)    

def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has 'username' and 'password' fields
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If user does not exist, raise error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # If password doesnt match, raise error
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Sucess! Create JWT Token
    access_token = auth.create_access_token(data={"user_id": user.id})
    
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}
