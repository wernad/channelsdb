from fastapi import APIRouter
from app.api.endpoints import (
    ping,
    annotations,
    channels,
    download,
    statistics,
)

api_router = APIRouter()
api_router.include_router(ping.router, tags=["health"], prefix="/health")
api_router.include_router(
    annotations.router, tags=["annotations"], prefix="/annotations"
)
api_router.include_router(channels.router, tags=["channels"], prefix="/channels")
api_router.include_router(download.router, tags=["export"], prefix="/download")
api_router.include_router(statistics.router, tags=["statistics"], prefix="/statistics")
