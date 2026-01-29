from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks # <-- Added BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, oauth2
from database import get_db, SessionLocal # <-- To get a New DB Session
from services import ai

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

#_______________________________________________________________
# 3. SUMMARIZE A DOCUMENT
@router.post("/{id}/summarize")
def summarize_document(
    id: int, 
    background_tasks: BackgroundTasks, # <--- Inject the tool
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # 1. Check if document exists & belongs to user
    document = db.query(models.Document).filter(models.Document.id == id, models.Document.owner_id == current_user.id).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    # 2. Add to Queue (Don't wait for it!)
    background_tasks.add_task(task_generate_summary, document.id, document.content)

    # 3. Reply Instantly
    return {"message": "Summary generation started in the background", "status": "processing"}

#_______________________________________________________________
# 4. ASYNC SUMMARIZE A DOCUMENT
def task_generate_summary(doc_id:int, content:str ):
    """
    this runs in the background to prevent blocking the main thread
    this opens its own DB session, talks to AIm and saves the summary
    """
    print(f"⏳ Background Task: Starting summary for Doc {doc_id}...")

    # talk to the AI service. this takes time but no one is waiting
    ai_summary = ai.summarize_document(content)
    
    # Create a new DB session
    db = SessionLocal()

    # Call the AI service to generate a summary
    try:
        # Fetch and update the document
        document=db.query(models.Document).filter(models.Document.id == doc_id).first()
        if document:
            document.summary = ai_summary
            db.commit()
            print(f"✅ Background Task: Doc {doc_id} updated successfully.")
    except Exception as e:
            print(f"❌ Background Task Failed: {e}")
    finally:
        db.close() # Always close the session
