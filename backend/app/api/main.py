from fastapi import APIRouter
from endpoints import annotations, assembly, channels, content, download, statistics

router = APIRouter()
router.include_router(annotations.router, tags=["annotations"], prefix="/annotations")
router.include_router(assembly.router, tags=["assembly"], prefix="/assembly")
router.include_router(channels.router, tags=[], prefix="/channels")
router.include_router(content.router, tags=[], prefix="/content")
router.include_router(download.router, tags=[], prefix="/download")
router.include_router(statistics.router, tags=[], prefix="/statistics")
