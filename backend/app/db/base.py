"""
The SQLAlchemy declarative base.

Every ORM model (User, Submission, etc.) inherits from this Base. Alembic
(our migration tool) also imports Base to detect what tables should exist —
so this file is the single source of truth connecting "what models exist"
to "what the database schema should look like."
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
