from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.database import get_db
from backend.app.config import get_settings
from backend.app.models.user import User
from backend.app.models.interview import Interview
from backend.app.models.sign_class import SignClass
from backend.app.models.candidate import Candidate
from backend.app.models.interviewer import Interviewer
from backend.app.schemas.user import UserResponse
from backend.app.schemas.interview import InterviewResponse
from backend.app.schemas.sign_class import SignClassResponse
from backend.app.seeds.seed_data import seed_database

router = APIRouter()
settings = get_settings()


@router.get("/health", tags=["System"])
def get_health(db: Session = Depends(get_db)):
    """Health check endpoint verifying backend and database connectivity."""
    db_connected = False
    dialect_name = "unknown"
    try:
        result = db.execute(text("SELECT 1")).scalar()
        db_connected = (result == 1)
        dialect_name = db.bind.dialect.name
    except Exception as e:
        db_connected = False

    return {
        "status": "healthy" if db_connected else "degraded",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": {
            "connected": db_connected,
            "dialect": dialect_name,
        },
        "phase": "Phase 1 & Phase 2 Complete",
        "message": "SignBridge Backend API is operational.",
    }


@router.get("/db/status", tags=["Database"])
def get_database_status(db: Session = Depends(get_db)):
    """Detailed database status returning record counts across all 11 MVP tables."""
    try:
        models_map = {
            "users": "SELECT count(*) FROM users",
            "candidates": "SELECT count(*) FROM candidates",
            "interviewers": "SELECT count(*) FROM interviewers",
            "interviews": "SELECT count(*) FROM interviews",
            "questions": "SELECT count(*) FROM questions",
            "interview_questions": "SELECT count(*) FROM interview_questions",
            "responses": "SELECT count(*) FROM responses",
            "transcripts": "SELECT count(*) FROM transcripts",
            "predictions": "SELECT count(*) FROM predictions",
            "sign_classes": "SELECT count(*) FROM sign_classes",
            "model_versions": "SELECT count(*) FROM model_versions",
        }
        counts = {}
        for table, query in models_map.items():
            try:
                cnt = db.execute(text(query)).scalar()
                counts[table] = cnt
            except Exception:
                counts[table] = "table not found"

        return {
            "database_url_dialect": db.bind.dialect.name,
            "all_mvp_tables_present": all(isinstance(v, int) for v in counts.values()),
            "table_record_counts": counts,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database inspection failed: {str(e)}",
        )


@router.post("/db/seed", tags=["Database"])
def seed_db_endpoint(db: Session = Depends(get_db)):
    """Seeds the database with initial MVP data fixtures."""
    try:
        counts = seed_database(db)
        return {
            "status": "success",
            "message": "Database successfully seeded with MVP test fixtures.",
            "counts": counts,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed database: {str(e)}",
        )


@router.get("/users", response_model=List[UserResponse], tags=["Users"])
def list_users(role: Optional[str] = None, db: Session = Depends(get_db)):
    """List registered users with optional role filtering (candidate, interviewer, admin)."""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()


@router.get("/interviews", response_model=List[InterviewResponse], tags=["Interviews"])
def list_interviews(status: Optional[str] = None, db: Session = Depends(get_db)):
    """List scheduled and active interviews."""
    query = db.query(Interview)
    if status:
        query = query.filter(Interview.status == status)
    return query.all()


@router.get("/sign-classes", response_model=List[SignClassResponse], tags=["Sign Vocabulary"])
def list_sign_classes(category: Optional[str] = None, db: Session = Depends(get_db)):
    """List supported ISL sign classes."""
    query = db.query(SignClass).filter(SignClass.is_active == True)
    if category:
        query = query.filter(SignClass.category == category)
    return query.all()

