import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, Base, engine
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database(db: Session = None) -> dict:
    close_after = False
    if db is None:
        db = SessionLocal()
        close_after = True

    try:
        # Create all tables if not already created
        Base.metadata.create_all(bind=engine)

        counts = {}

        # 1. Sign Classes
        sign_classes_data = [
            {"label": "hello", "display_name": "Hello / Greeting", "category": "greetings", "description": "Open hand waving or moving outwards from forehead"},
            {"label": "thank_you", "display_name": "Thank You", "category": "greetings", "description": "Flat hand moving forward from chin"},
            {"label": "yes", "display_name": "Yes / Agree", "category": "answers", "description": "Fist nodding up and down"},
            {"label": "no", "display_name": "No / Disagree", "category": "answers", "description": "Index, middle, and thumb tapping together"},
            {"label": "help", "display_name": "Help / Support", "category": "common", "description": "Closed fist on flat palm moving upwards"},
            {"label": "experience", "display_name": "Work Experience", "category": "interview", "description": "Hand sweeping down cheek or chest"},
            {"label": "python", "display_name": "Python Language", "category": "interview", "description": "Two curved fingers resembling snake gesture"},
            {"label": "project", "display_name": "Project / Build", "category": "interview", "description": "Hands outlining blueprint or pyramid"},
            {"label": "done", "display_name": "Finished / Done", "category": "answers", "description": "Both open hands turning outward"},
            {"label": "repeat", "display_name": "Please Repeat", "category": "common", "description": "Curved hand flipping backwards"},
        ]

        created_sign_classes = []
        for item in sign_classes_data:
            existing = db.query(SignClass).filter(SignClass.label == item["label"]).first()
            if not existing:
                sc = SignClass(**item)
                db.add(sc)
                created_sign_classes.append(sc)
            else:
                created_sign_classes.append(existing)
        db.commit()
        counts["sign_classes"] = db.query(SignClass).count()

        # 2. Model Versions
        mv = db.query(ModelVersion).filter(ModelVersion.version_tag == "v1.0.0-isolated-signs").first()
        if not mv:
            mv = ModelVersion(
                version_tag="v1.0.0-isolated-signs",
                model_type="isolated_classifier",
                weights_path_or_url="models/weights/isl_isolated_v1.onnx",
                accuracy_metrics='{"val_accuracy": 0.942, "macro_f1": 0.931, "classes_count": 10}',
                is_active=True,
            )
            db.add(mv)
            db.commit()
        counts["model_versions"] = db.query(ModelVersion).count()

        # 3. Users (Admin, Interviewer, Candidate)
        # Admin
        admin_user = db.query(User).filter(User.email == "admin@signbridge.ai").first()
        if not admin_user:
            admin_user = User(
                email="admin@signbridge.ai",
                password_hash="$2b$12$e80z8v1gJdD9WzB3rK2nYeGzLhMhR6eQ8wP9x.AdminHashPlaceholder",
                full_name="SignBridge Admin",
                role="admin",
                is_active=True,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

        # Interviewer User & Profile
        interviewer_user = db.query(User).filter(User.email == "interviewer@techcorp.com").first()
        if not interviewer_user:
            interviewer_user = User(
                email="interviewer@techcorp.com",
                password_hash="$2b$12$e80z8v1gJdD9WzB3rK2nYeGzLhMhR6eQ8wP9x.InterviewerHashPlaceholder",
                full_name="Sarah Chen",
                role="interviewer",
                is_active=True,
            )
            db.add(interviewer_user)
            db.commit()
            db.refresh(interviewer_user)

        interviewer_profile = db.query(Interviewer).filter(Interviewer.user_id == interviewer_user.id).first()
        if not interviewer_profile:
            interviewer_profile = Interviewer(
                user_id=interviewer_user.id,
                department="Engineering",
                designation="Lead Engineering Manager",
            )
            db.add(interviewer_profile)
            db.commit()
            db.refresh(interviewer_profile)

        # Candidate User & Profile
        candidate_user = db.query(User).filter(User.email == "rahul.candidate@gmail.com").first()
        if not candidate_user:
            candidate_user = User(
                email="rahul.candidate@gmail.com",
                password_hash="$2b$12$e80z8v1gJdD9WzB3rK2nYeGzLhMhR6eQ8wP9x.CandidateHashPlaceholder",
                full_name="Rahul Verma",
                role="candidate",
                is_active=True,
            )
            db.add(candidate_user)
            db.commit()
            db.refresh(candidate_user)

        candidate_profile = db.query(Candidate).filter(Candidate.user_id == candidate_user.id).first()
        if not candidate_profile:
            candidate_profile = Candidate(
                user_id=candidate_user.id,
                phone="+91-9876543210",
                education="B.Tech in Computer Science, IIT Madras",
                skills="Python, FastAPI, React, Machine Learning, Indian Sign Language (Native)",
                resume_url="https://signbridge.ai/resumes/rahul_verma_cv.pdf",
                preferred_communication_mode="isl",
            )
            db.add(candidate_profile)
            db.commit()
            db.refresh(candidate_profile)

        counts["users"] = db.query(User).count()
        counts["interviewers"] = db.query(Interviewer).count()
        counts["candidates"] = db.query(Candidate).count()

        # 4. Bank of Questions
        questions_data = [
            {
                "question_text": "Could you introduce yourself and tell us about your recent software projects?",
                "category": "introductory",
                "difficulty": "easy",
                "interviewer_id": interviewer_profile.id,
            },
            {
                "question_text": "How do you design scalable REST APIs and handle real-time streaming data?",
                "category": "technical",
                "difficulty": "medium",
                "interviewer_id": interviewer_profile.id,
            },
            {
                "question_text": "Describe a difficult technical bug you solved and your debugging methodology.",
                "category": "technical",
                "difficulty": "hard",
                "interviewer_id": interviewer_profile.id,
            },
        ]
        created_questions = []
        for qd in questions_data:
            existing = db.query(Question).filter(Question.question_text == qd["question_text"]).first()
            if not existing:
                q = Question(**qd)
                db.add(q)
                created_questions.append(q)
            else:
                created_questions.append(existing)
        db.commit()
        counts["questions"] = db.query(Question).count()

        # 5. Scheduled Interview
        now = datetime.now(timezone.utc)
        interview = db.query(Interview).filter(Interview.meeting_room_id == "signbridge-demo-room-101").first()
        if not interview:
            interview = Interview(
                title="Full Stack Software Engineer - Technical Assessment",
                candidate_id=candidate_profile.id,
                interviewer_id=interviewer_profile.id,
                scheduled_start=now + timedelta(days=1),
                duration_minutes=45,
                status="scheduled",
                meeting_room_id="signbridge-demo-room-101",
                notes="Candidate communicates natively via ISL with SignBridge real-time translator active.",
            )
            db.add(interview)
            db.commit()
            db.refresh(interview)
        counts["interviews"] = db.query(Interview).count()

        # 6. Interview Questions
        for idx, q in enumerate(created_questions, start=1):
            iq = (
                db.query(InterviewQuestion)
                .filter(
                    InterviewQuestion.interview_id == interview.id,
                    InterviewQuestion.question_id == q.id,
                )
                .first()
            )
            if not iq:
                iq = InterviewQuestion(
                    interview_id=interview.id,
                    question_id=q.id,
                    question_order=idx,
                    custom_prompt=f"Order {idx}: {q.question_text}",
                    status="pending" if idx > 1 else "active",
                )
                db.add(iq)
        db.commit()
        counts["interview_questions"] = db.query(InterviewQuestion).count()

        # 7. Candidate Response to first question
        first_iq = (
            db.query(InterviewQuestion)
            .filter(InterviewQuestion.interview_id == interview.id)
            .order_by(InterviewQuestion.question_order)
            .first()
        )
        if first_iq:
            resp = db.query(Response).filter(Response.interview_question_id == first_iq.id).first()
            if not resp:
                resp = Response(
                    interview_question_id=first_iq.id,
                    candidate_id=candidate_profile.id,
                    raw_sign_data='{"signs_detected": ["hello", "experience", "python", "project"]}',
                    final_text_response="Hello, I have extensive experience building scalable Python and React projects.",
                    audio_caption_text=None,
                )
                db.add(resp)
                db.commit()
        counts["responses"] = db.query(Response).count()

        # 8. Transcripts (both Interviewer spoken caption and Candidate sign translation)
        t_interviewer = (
            db.query(Transcript)
            .filter(
                Transcript.interview_id == interview.id,
                Transcript.speaker_role == "interviewer",
            )
            .first()
        )
        if not t_interviewer:
            t_interviewer = Transcript(
                interview_id=interview.id,
                speaker_role="interviewer",
                speaker_id=interviewer_user.id,
                message_type="speech_caption",
                content="Hello Rahul, welcome to the SignBridge technical interview. Let's begin!",
                timestamp=now,
                confidence_score=0.98,
            )
            db.add(t_interviewer)
            db.commit()
            db.refresh(t_interviewer)

        t_candidate = (
            db.query(Transcript)
            .filter(
                Transcript.interview_id == interview.id,
                Transcript.speaker_role == "candidate",
            )
            .first()
        )
        if not t_candidate:
            t_candidate = Transcript(
                interview_id=interview.id,
                speaker_role="candidate",
                speaker_id=candidate_user.id,
                message_type="sign_prediction",
                content="Hello! Thank you. I am glad to meet you and ready to demonstrate my experience.",
                timestamp=now + timedelta(seconds=12),
                confidence_score=0.95,
            )
            db.add(t_candidate)
            db.commit()
            db.refresh(t_candidate)
        counts["transcripts"] = db.query(Transcript).count()

        # 9. Predictions
        hello_class = db.query(SignClass).filter(SignClass.label == "hello").first()
        pred = db.query(Prediction).filter(Prediction.interview_id == interview.id).first()
        if not pred and t_candidate:
            pred = Prediction(
                interview_id=interview.id,
                transcript_id=t_candidate.id,
                sign_class_id=hello_class.id if hello_class else None,
                predicted_sign="hello",
                confidence_score=0.965,
                is_low_confidence=False,
                latency_ms=135.5,
                raw_landmark_summary='{"wrist": [0.52, 0.74, 0.0], "landmarks_count": 21}',
            )
            db.add(pred)
            db.commit()
        counts["predictions"] = db.query(Prediction).count()

        logger.info(f"Database seed successful: {counts}")
        return counts

    finally:
        if close_after:
            db.close()


if __name__ == "__main__":
    seed_database()
