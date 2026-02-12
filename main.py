from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# from slowapi import _rate_limit_exceeded_handler # <-- Import the handler for rate limit exceeded
from fastapi.responses import JSONResponse # <-- Import JSONResponse to create a custom response for rate limit exceeded
from slowapi.errors import RateLimitExceeded # <-- Import the exception for rate limit exceeded
from limiter import limiter # <-- Import the limiter instance we set up
import models
from database import engine
from routers import users, auth, documents


# CREATE THE FASTAPI INSTANCE / THE APP
app=FastAPI()

# DATABASE SETUP: AUTO-CREATE TABLES 
models.Base.metadata.create_all(bind = engine)


app.state.limiter = limiter # <-- Attach the limiter to the app state

# --- CORSE SECURITY MIDDLEWARE ---
# define who can talk to our API from other origins
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "https://docusafe-frontend.onrender.com"
]

# CORS (Optional, but good for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Only allow these domains
    allow_credentials=True, # Allow cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE"], # Explicitly list allowed methods
    allow_headers=["Authorization", "Content-Type"], # Explicitly list allowed headers
)

# CONNECT ROUTERs
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(documents.router)

# Define the custom handler for rate limit exceeded
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """
    catch the 429 error and return a clean custom JSON response instead of the default HTML response from slowapi
    
    :param request: Description
    :type request: Request
    :param exc: Description
    :type exc: RateLimitExceeded
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate Limit Exceeded",
            "detail": f"Too Many Requests...{exc.detail}"
        }
    )

# Register Custom exception handler for rate limit exceeded
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

@app.get("/")
async def root():
    return {"message": "Welcome to the DocuSafe API"}