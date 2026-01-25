from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# 1. GET ALL MY DOCUMENTS
# FIX: Changed 'current_user: int' to 'current_user: models.User'
@router.get("/", response_model=List[schemas.DocumentResponse])
def get_documents(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # Now the IDE knows current_user is a User Object, so .id is valid
    documents = db.query(models.Document).filter(models.Document.owner_id == current_user.id).all()
    return documents

# 2. CREATE A DOCUMENT
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DocumentResponse)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # FIX: Changed .dict() to .model_dump() for Pydantic V2
    new_document = models.Document(owner_id=current_user.id, **document.model_dump())
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document