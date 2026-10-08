"""
Importing every model here means a single `from app import models` (used
by Alembic's env.py) is enough to register all tables with Base.metadata —
no model gets silently forgotten by a migration.
"""

from app.models.user import User  # noqa: F401
