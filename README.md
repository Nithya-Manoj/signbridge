# SignBridge 🤟

> Real-time Indian Sign Language (ISL) recognition and bidirectional video interview platform for Deaf / Hard-of-Hearing (DHH) candidates and hearing interviewers.

---

## 📌 Implementation Status

| Phase | Description | Status | Exit Criteria Verification |
|---|---|---|---|
| **Phase 1** | Environment Setup (Python, Node, PostgreSQL, Git, Editor config) | **Completed** | Repo boots; FastAPI & React apps scaffolded and functional |
| **Phase 2** | Database Architecture & MVP Schema (11 tables) | **Completed** | Tables created, foreign keys enforced, seed data loaded, 10/10 tests pass |
| **Phase 3** | Backend Core (FastAPI auth, interviews, transcripts CRUD) | Next Up | CRUD endpoints tested for users, interviews, transcripts |

---

## 🗄️ Database Architecture (PRD Section 7 — 11 MVP Tables)

The database schema is managed via **SQLAlchemy** and **Alembic** migrations (`001_initial_mvp_schema`):

1. **`users`** — Candidates, interviewers, and administrators with hashed credentials and role-based permissions (`FR-01`, `FR-02`).
2. **`candidates`** — Detailed profile for DHH candidates: education, skills, resume URL, and preferred communication mode (`isl`, `speech_caption`, `text`, `FR-03`).
3. **`interviewers`** — Interviewer profile: corporate department and designation.
4. **`interviews`** — 1:1 scheduled interview rooms with candidate & interviewer references, timestamps, meeting room IDs, and status (`FR-04`, `FR-06`).
5. **`questions`** — Interview question bank categorized by technical/behavioral and difficulty (`FR-05`).
6. **`interview_questions`** — Ordered questions linked to specific interview sessions.
7. **`responses`** — Candidate responses recording sign metadata, transcripts, and final text answers.
8. **`transcripts`** — Full timestamped bidirectional transcript logging both interviewer speech captions and candidate sign translations (`FR-09`).
9. **`predictions`** — Real-time ISL recognition outputs containing predicted signs, confidence scores, latency (ms), and low-confidence flags (`FR-08`, `FR-10`).
10. **`sign_classes`** — Catalog of supported Indian Sign Language isolated signs (e.g. *hello*, *thank_you*, *yes*, *no*, *experience*, *python*).
11. **`model_versions`** — Machine learning model registry with version tags, weights location, and validation accuracy metrics.

---

## 🚀 Getting Started

### 1. Backend Setup & Run

Activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

Apply database migrations:
```powershell
python -m alembic upgrade head
```

Seed initial MVP test data:
```powershell
python -m backend.app.seeds.seed_data
```

Start the FastAPI application:
```powershell
python main.py
```
- Interactive Dashboard: **`http://localhost:8000/`**
- Swagger API Documentation: **`http://localhost:8000/docs`**
- Health API: **`http://localhost:8000/api/health`**
- Database Table Status: **`http://localhost:8000/api/db/status`**

### 2. Frontend Setup (React + Vite)

```powershell
cd frontend
npm install
npm run dev
```
The React development server runs on **`http://localhost:5173`**.

---

## 🧪 Automated Testing

Run the full automated test suite (covering all 11 database tables, relationship integrity, cascading rules, and API endpoints):

```powershell
pytest backend/tests/ -v
```
All 10 tests pass with 100% success rate.
