from fastapi import APIRouter
from app.api.endpoints import (
    annotations,
    assembly,
    channels,
    content,
    download,
    statistics,
)

api_router = APIRouter()
api_router.include_router(annotations.router, tags=["annotations"], prefix="/annotations")
api_router.include_router(assembly.router, tags=["assembly"], prefix="/assembly")
api_router.include_router(channels.router, tags=[], prefix="/channels")
api_router.include_router(content.router, tags=[], prefix="/content")
api_router.include_router(download.router, tags=[], prefix="/download")
api_router.include_router(statistics.router, tags=[], prefix="/statistics")
