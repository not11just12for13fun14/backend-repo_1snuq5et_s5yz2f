from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import os
from database import db, database_url, database_name

app = FastAPI(title="Appealio API", version="1.0.0")

# CORS setup - allow frontend dev server
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if frontend_url == "*" else frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> Dict[str, Any]:
    return {"message": "Appealio backend is running", "status": "ok"}

@app.get("/test")
def test_db() -> Dict[str, Any]:
    try:
        collections = []
        conn_status = "disconnected"
        if db is not None:
            collections = db.list_collection_names()
            # lightweight ping by listing collections succeeds if connected
            conn_status = "connected"
        return {
            "backend": "FastAPI",
            "database": "MongoDB",
            "database_url": database_url or "not set",
            "database_name": database_name or "not set",
            "connection_status": conn_status,
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "FastAPI",
            "database": "MongoDB",
            "error": str(e)
        }
