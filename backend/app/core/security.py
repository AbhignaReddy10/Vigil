"""
Security utilities: password hashing and JWT token handling.

Two separate concerns live here, deliberately:
1. Hashing passwords (so we NEVER store a password in plain text — even
   we, the developers, should not be able to read a user's password).
2. Issuing and verifying JWT tokens (so a user logs in once and then
   proves who they are on every subsequent request without re-sending
   their password each time).
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt is the industry-standard password hashing algorithm — slow by
# design, which is exactly what you want (it makes brute-forcing stolen
# password hashes impractically expensive).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def hash_password(plain_password: str) -> str:
    """Turn a plain-text password into a one-way hash for storage."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's password against the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Create a signed JWT for an authenticated user.

    'subject' is typically the user's email or ID. The token is signed
    with our secret key, so we can trust it wasn't tampered with — but
    it is NOT encrypted, so never put sensitive data inside it.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """Verify a JWT and return its subject (user identifier), or None if invalid."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
