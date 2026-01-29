from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import oauth2
import models
import schemas
import utils
from database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# 1. Create a new user (Now with Hashing and Security)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) # Return the Safe Response Schema
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user with the same email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before storing it
    hashed_password = utils.hash_password(user.password)

    # Determine Status based on experience
    determined_status = "Pro" if user.experience_years >= 1 else "Intern"

    # Create User instance / Create DB Model
    db_user = models.User(
        name = user.name,
        email = user.email,
        password = hashed_password,
        experience_years = user.experience_years,
        status = determined_status
    )

    # Add and commit to the database
    db.add(db_user) # Add to DB Session
    db.commit() # Save to DB
    db.refresh(db_user) # Refresh to get the new ID and other generated fields
    return db_user # Return the created user (will be serialized by Pydantic)


# Get Users Endpoints 
# GET /users/me - Get current logged-in user
@router.get("/me", response_model=schemas.UserResponse) # Return Safe Response Schema
def get_current_user(current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user # Return the current logged-in user (will be serialized by Pydantic)

# 2. GET ALL Users (Returns List of Safe Schemas)
@router.get("/", response_model=List[schemas.UserResponse]) # Return List of Safe Response Schemas
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all() # Query all users from the database
    return users # Return the list of users (will be serialized by Pydantic)

# 3. GET User by ID (Returns Safe Schema)
@router.get("/{user_id}", response_model = schemas.UserResponse) # Return Safe Response Schema
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first() # Query user by 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user # Return the user (will be serialized by Pydantic)

# 4. Update User by ID (Using UserCreate implies replacing all fields including password)
@router.put("/{user_id}", response_model=schemas.UserResponse) # Return Safe Response Schema
def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first() # Query user by ID
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields
    # Note: In a real application, you might want to allow partial updates (PATCH) instead of full replacement (PUT)
    db_user.name = updated_user.name
    db_user.email = updated_user.email
    db_user.experience_years = updated_user.experience_years

    # Update status based on experience
    db_user.status = "Pro" if updated_user.experience_years >= 1 else "Intern"

    # Important: Since this is a PUT, we replace the password as well
    db_user.password = utils.hash_password(updated_user.password)   

    db.commit() # Save changes to DB
    db.refresh(db_user) # Refresh to get updated data
    return db_user # Return the updated user (will be serialized by Pydantic)

# 5. Delete User by ID
@router.delete("/{user_id}") # Return Safe Response Schema
def delete_user(user_id :int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first() # Query user by ID
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user) # Delete the user
    db.commit() # Commit the deletion
    return {"message": "User {user_id} deleted successfully."}