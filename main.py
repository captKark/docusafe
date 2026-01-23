from fastapi import FastAPI
import models
from database import engine
from routers import users, auth

# 1. The Architect: Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. Wiring: Connect the Router
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Docusafe API is running"}