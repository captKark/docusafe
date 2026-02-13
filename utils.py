from passlib.context import CryptContext
from pypdf import PdfReader
from fastapi import HTTPException, UploadFile

# Setting up the Hashing Context for password hashing
# We tell it to use bcrypt algorithm for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain password (Create)
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# Function to verify a plain password against a hashed password (Authenticate) (Login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#---------- PDF Text Extraction Utility ----------

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Reads a PDF file upload and returns the raw text content as a string.
    """
    try:
        reader = PdfReader(file.file) # try to read the PDF to ensure it's valid
        text=""
        
        # Loop through each page and extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text: # Check if text was extracted successfully
                text += page_text + "\n" # Add a newline after each page's text
        if not text.strip(): # If no text was extracted, raise an error
            raise ValueError("No readable text can be extracted from this PDF. It may be scanned or image-based.")           
        return text

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to PDF: {str(e)}") 