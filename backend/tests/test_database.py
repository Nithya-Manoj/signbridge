import pytest
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from backend.app.database import Base
from backend.app.models.user import User
from backend.app.models.candidate import Candidate
from backend.app.models.interviewer import Interviewer
from backend.app.models.interview import Interview
from backend.app.models.question import Question, InterviewQuestion
from backend.app.models.response import Response
from backend.app.models.transcript import Transcript
from backend.app.models.sign_class import SignClass
from backend.app.models.prediction import Prediction
from backend.app.models.model_version import ModelVersion
from backend.app.seeds.seed_data import seed_database


@pytest.fixture(scope="function")
def test_db():
    """In-memory SQLite database for test isolation with foreign keys enforced."""
    engine = create_engine("sqlite:///:memory:", echo=False)

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_seed_database_loads_all_mvp_tables(test_db):
    """Verify seed_database populates all 11 MVP tables."""
    counts = seed_database(test_db)

    assert counts["users"] >= 3
    assert counts["candidates"] >= 1
    assert counts["interviewers"] >= 1
    assert counts["interviews"] >= 1
    assert counts["questions"] >= 3
    assert counts["interview_questions"] >= 3
    assert counts["responses"] >= 1
    assert counts["transcripts"] >= 2
    assert counts["predictions"] >= 1
    assert counts["sign_classes"] >= 10
    assert counts["model_versions"] >= 1

    # Verify candidate relationship to user
    candidate = test_db.query(Candidate).first()
    assert candidate is not None
    assert candidate.user is not None
    assert candidate.user.role == "candidate"
    assert candidate.preferred_communication_mode == "isl"

    # Verify interviewer relationship
    interviewer = test_db.query(Interviewer).first()
    assert interviewer is not None
    assert interviewer.user is not None
    assert interviewer.user.role == "interviewer"

    # Verify interview relationships
    interview = test_db.query(Interview).first()
    assert interview is not None
    assert interview.candidate.id == candidate.id
    assert interview.interviewer.id == interviewer.id
    assert len(interview.interview_questions) >= 3
    assert len(interview.transcripts) >= 2
    assert len(interview.predictions) >= 1

    # Verify prediction details
    pred = test_db.query(Prediction).first()
    assert pred.predicted_sign == "hello"
    assert pred.confidence_score > 0.9
    assert pred.is_low_confidence is False
    assert pred.sign_class.label == "hello"


def test_unique_user_email_enforced(test_db):
    """Enforce unique constraint on users.email."""
    u1 = User(
        email="duplicate@signbridge.ai",
        password_hash="hash1",
        full_name="User One",
        role="candidate",
    )
    test_db.add(u1)
    test_db.commit()

    u2 = User(
        email="duplicate@signbridge.ai",
        password_hash="hash2",
        full_name="User Two",
        role="interviewer",
    )
    test_db.add(u2)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_foreign_key_enforcement(test_db):
    """Enforce foreign key checks on candidate with non-existent user."""
    orphan_candidate = Candidate(
        user_id="non-existent-user-uuid",
        education="B.Sc",
    )
    test_db.add(orphan_candidate)
    with pytest.raises(IntegrityError):
        test_db.commit()
    test_db.rollback()


def test_interview_cascade_delete(test_db):
    """Enforce cascading delete from interview to interview questions and transcripts."""
    seed_database(test_db)
    interview = test_db.query(Interview).first()
    interview_id = interview.id

    assert test_db.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).count() > 0
    assert test_db.query(Transcript).filter(Transcript.interview_id == interview_id).count() > 0

    test_db.delete(interview)
    test_db.commit()

    # InterviewQuestions and Transcripts should be cascade deleted
    assert test_db.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview_id).count() == 0
    assert test_db.query(Transcript).filter(Transcript.interview_id == interview_id).count() == 0

