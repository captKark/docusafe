from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas, oauth2
from database import get_db, SessionLocal
from services import ai
from utils import extract_text_from_pdf

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# 1. GET DOCUMENTS (List)
@router.get("/", response_model=List[schemas.DocumentResponse])
def get_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    results = db.query(models.Document).filter(models.Document.owner_id == current_user.id)

    if search:
        results = results.filter(models.Document.title.contains(search))

    results = results.limit(limit).offset(skip).all()
    return results

# ___________________________________________________________________

# 2. UPLOAD A DOCUMENT (New!) 🚀
@router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=schemas.DocumentResponse)
def upload_document(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    """
    Uploads a PDF, extracts text, and saves it to the database.
    """
    # A. Validate File Type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")

    # B. Extract Text
    try:
        content = extract_text_from_pdf(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")
    
    # C. Save to Database
    new_doc = models.Document(
        title=file.filename, # Use filename as the title
        content=content,
        owner_id=current_user.id
    )
    
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)
    
    return new_doc

# ___________________________________________________________________

# 3. CREATE A DOCUMENT (Manual Text Input)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.DocumentResponse)
def create_document(
    document: schemas.DocumentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    new_document = models.Document(owner_id=current_user.id, **document.model_dump())
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document

# _______________________________________________________________

# 4. SUMMARIZE A DOCUMENT
@router.post("/{id}/summarize")
def summarize_document(
    id: int, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(oauth2.get_current_user)
):
    document = db.query(models.Document).filter(models.Document.id == id, models.Document.owner_id == current_user.id).first()

    if not document:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    background_tasks.add_task(task_generate_summary, document.id, document.content)

    return {"message": "Summary generation started in the background", "status": "processing"}

# _______________________________________________________________

# 5. ASYNC BACKGROUND TASK
def task_generate_summary(doc_id: int, content: str):
    print(f"⏳ Background Task: Starting summary for Doc {doc_id}...")
    
    # 1. Generate Summary
    ai_summary = ai.summarize_document(content)
    
    # 2. Save to DB
    db = SessionLocal()
    try:
        document = db.query(models.Document).filter(models.Document.id == doc_id).first()
        if document:
            document.summary = ai_summary
            db.commit()
            print(f"✅ Background Task: Doc {doc_id} updated successfully.")
    except Exception as e:
        print(f"❌ Background Task Failed: {e}")
    finally:
        db.close()