import pytest
from backend.app.database import SessionLocal
from backend.app.seeds.seed_data import seed_database
from backend.app.api.routes import (
    get_health,
    get_database_status,
    seed_db_endpoint,
    list_users,
    list_interviews,
    list_sign_classes,
)
from backend.app.main import home


@pytest.fixture(scope="module")
def db_session():
    seed_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_home_endpoint():
    result = home()
    assert "SignBridge" in result
    assert "Phase 1: Environment" in result
    assert "Phase 2: Database MVP Schema" in result


def test_health_endpoint(db_session):
    result = get_health(db_session)
    assert result["status"] == "healthy"
    assert result["database"]["connected"] is True
    assert "SignBridge" in result["app_name"]


def test_database_status_endpoint(db_session):
    result = get_database_status(db_session)
    assert result["all_mvp_tables_present"] is True
    counts = result["table_record_counts"]
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


def test_list_users(db_session):
    users = list_users(None, db_session)
    assert len(users) >= 3
    roles = {u.role for u in users}
    assert "candidate" in roles
    assert "interviewer" in roles
    assert "admin" in roles

    candidate_users = list_users("candidate", db_session)
    assert all(u.role == "candidate" for u in candidate_users)


def test_list_interviews(db_session):
    interviews = list_interviews(None, db_session)
    assert len(interviews) >= 1
    first_interview = interviews[0]
    assert first_interview.meeting_room_id == "signbridge-demo-room-101"
    assert first_interview.candidate is not None
    assert first_interview.interviewer is not None
    assert len(first_interview.interview_questions) >= 3


def test_list_sign_classes(db_session):
    classes = list_sign_classes(None, db_session)
    assert len(classes) >= 10
    labels = {c.label for c in classes}
    assert "hello" in labels
    assert "thank_you" in labels
    assert "yes" in labels
    assert "no" in labels
