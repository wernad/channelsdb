from fastapi import APIRouter
from app.api.endpoints import (
    annotations,
    channels,
    content,
    download,
    statistics,
)

api_router = APIRouter()
api_router.include_router(annotations.router, tags=["annotations"], prefix="/annotations")
api_router.include_router(channels.router, tags=["channels"], prefix="/channels")
api_router.include_router(content.router, tags=["content"], prefix="/content")
api_router.include_router(download.router, tags=["export"], prefix="/download")
api_router.include_router(statistics.router, tags=["statistics"], prefix="/statistics")
