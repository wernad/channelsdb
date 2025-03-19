from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping() -> None:
    """Endpoint to test connection."""
    return None
