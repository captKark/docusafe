from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import users, auth, documents


# CREATE THE FASTAPI INSTANCE / THE APP
app=FastAPI()

# DATABASE SETUP: AUTO-CREATE TABLES 
models.Base.metadata.create_all(bind = engine)

# CORS (Optional, but good for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any Frontend to talk to us/  Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CONNECT ROUTERs
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the DocuSafe API"}