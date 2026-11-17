from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["Health"])

DEFAULT_HEALTH_CHECK_RESPONSE: dict[int | str, dict[str, Any]] = {
    503: {
        "description": "Database unavailable",
        "content": {
            "application/json": {
                "example": {
                    "status": "unavailable",
                    "database": "disconnected",
                }
            }
        },
    }
}

@router.get("/health/ready", responses=DEFAULT_HEALTH_CHECK_RESPONSE)
def readiness_check(db: Annotated[Session, Depends(get_db)]):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except SQLAlchemyError as err:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unavailable",
                "database": "disconnected",
            },
        ) from err
