
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="API para gerenciamento e controle de estoque.",
    version=settings.APP_VERSION,
    debug=settings.APP_DEBUG,
)

app.include_router(api_router)
