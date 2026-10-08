"""
API-facing schemas for users.

Why these are separate from app/models/user.py: the database model has a
hashed_password field — that should NEVER be sent back in an API response.
UserOut deliberately excludes it. This separation is what prevents the
classic bug where a password hash accidentally leaks into a JSON response.
"""

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.user import UserRole


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    full_name: str
    role: UserRole


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
