"""
Aggregates every endpoint module under app/api/v1/endpoints/ into one
router. As Vigil grows (analyzer endpoints in Month 1, history in Month 2,
monitoring in Month 5...), each new feature gets its own endpoints file
and one new line here — main.py never needs to change.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
