import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

db_url = settings.DATABASE_URL

# Handle connect args for SQLite
connect_args = {}
if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=settings.DEBUG and False,  # set True if detailed SQL queries logging is required
    pool_pre_ping=True,
)

# Enforce foreign keys for SQLite
if db_url.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency to yield database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

