from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, oauth2
from database import get_db

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# 1. GET DOCUMENTS WITH QUERY PARAMETERS
@router.get("/", response_model=List[schemas.DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user), # Ensure user is authenticated
    limit: int = 10,            # Default. Show 10 documents
    skip: int = 0,               # Default. Skip 0. Start from the beginning
    search: Optional[str]= ""   # Default. No search filter initially
):
    # Base Query: Fetch documents owned by the current user
    # we build the query step by step
    results = db.query(models.Document).filter(models.Document.owner_id == current_user.id)

    # Apply Search Filter if provided by the user
    # SQL translation: WHERE title LIKE '%search%'
    if search:
        results = results.filter(models.Document.title.contains(search))

    # Apply Pagination: Limit and Offset
    # SQL translation: LIMIT 10 OFFSET 0
    results=results.limit(limit).offset(skip).all() # Execute the query and fetch results

    return results # Return the list of documents to the user

#___________________________________________________________________

# 2. CREATE A DOCUMENT
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DocumentResponse)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # FIX: Changed .dict() to .model_dump() for Pydantic V2
    new_document = models.Document(owner_id=current_user.id, **document.model_dump())
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document