from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# 1. Absolute Imports (The Professional Way)
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# 2. Update functions to use 'schemas.UserPayLoad'
@router.post("/", response_model=None) 
def create_user(user: schemas.UserPayLoad, db: Session = Depends(get_db)):
    determined_status = "Intern"
    if user.experience_years >= 1:
        determined_status = "Pro"

    db_user = models.User(
        name=user.name, 
        experience_years=user.experience_years, 
        status=determined_status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=None)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(user_id: int, updated_user: schemas.UserPayLoad, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = updated_user.name
    db_user.experience_years = updated_user.experience_years
    
    if db_user.experience_years >= 1:
        db_user.status = "Pro"
    else:
        db_user.status = "Intern"
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}