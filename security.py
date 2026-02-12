import os
from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

# --- THE FIX ---
# We use os.environ.get() with a check, OR we just cast it to satisfy the linter.
# But the cleanest way for Type Checkers is this:
SECRET_KEY = os.getenv("SECRET_KEY")

# Explicitly check and raise error if missing
if SECRET_KEY is None:
    raise ValueError("❌ FATAL ERROR: No SECRET_KEY found in .env file!")

# ----------------

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # The linter might still complain because SECRET_KEY is global.
    # To silence it 100%, we assert it again inside the function:
    assert SECRET_KEY is not None 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt