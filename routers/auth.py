from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
import models, schemas, utils, security
from limiter import limiter # <-- Import the limiter instance we set up

# Create the router for authentication 
router = APIRouter(
    tags=["Authentication"]
)
# Login Endpoint
@router.post("/login", response_model=schemas.Token)    
@limiter.limit("5/minute") # <-- Apply rate limit to this endpoint (5 requests per minute)
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm has 'username' and 'password' fields
    # Note: You MUST add 'request: Request' to the function arguments 
    # so slowapi knows who to ban!
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    # If user does not exist, raise error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # If password doesnt match, raise error
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # Sucess! Create JWT Token
    access_token = security.create_access_token(data={"user_id": user.id})
    
    # Return the token
    return {"access_token": access_token, "token_type": "bearer"}
