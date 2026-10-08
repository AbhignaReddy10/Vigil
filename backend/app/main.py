"""
Vigil — main FastAPI application entrypoint.

This file stays deliberately thin: it creates the app, sets up CORS, and
mounts the versioned API router. All real logic lives in app/api/,
app/services/, and app/models/ — main.py should never grow large.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=f"{settings.project_name} API",
    description="Adaptive, self-monitoring multi-channel threat detection platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root():
    """Basic landing endpoint — confirms the API is alive."""
    return {
        "project": settings.project_name,
        "status": "online",
        "environment": settings.environment,
    }
