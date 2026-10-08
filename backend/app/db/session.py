"""
Database engine and session management.

A "session" is a single conversation with the database — you open one,
do some work (queries, inserts), commit or roll back, then close it.

get_db() is a FastAPI dependency: FastAPI calls it before your endpoint
runs, hands your endpoint the session via dependency injection, then
automatically closes it after — even if your endpoint raised an error.
This pattern (used throughout the app) means no endpoint ever has to
remember to manually close a database connection.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# connect_args is SQLite-specific (allows use across async FastAPI request
# threads); it's harmless and ignored when running against real Postgres.
connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(settings.database_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
