"""Health check endpoint."""

from fastapi import APIRouter
from sqlalchemy import text

from app.core.config import get_settings
from app.core.database import async_session_maker

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Health check with database connectivity test."""
    settings = get_settings()
    db_status = "unknown"

    try:
        async with async_session_maker() as session:
            await session.execute(text("SELECT 1"))
            db_status = "connected"
    except Exception:
        db_status = "disconnected"

    status = "healthy" if db_status == "connected" else "degraded"

    return {
        "status": status,
        "service": settings.app_name,
        "environment": settings.app_env,
        "database": db_status,
    }
