"""
Health check endpoint — cloud platforms (Azure, Railway) ping this to
confirm the service is alive and restart it automatically if it isn't.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}
