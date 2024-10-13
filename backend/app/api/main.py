from fastapi import FastAPI, APIRouter
from endpoints import annotations, assembly, channels, content, download, statistics

router = APIRouter()
router.include_router(annotations.router, prefix="/annotations")
router.include_router(assembly.router, prefix="/assembly")
router.include_router(channels.router, prefix="/channels")
router.include_router(content.router, prefix="/content")
router.include_router(download.router, prefix="/download")
router.include_router(statistics.router, prefix="/statistics")

app = FastAPI(
    title="ChannelsDB 2.1 API",
    contact={"name": "Tomáš Raček", "email": "tomas.racek@ceitec.muni.cz"},
    redoc_url=None,
    docs_url="/",
    version="beta",
    swagger_ui_parameters={"syntaxHighlight": False, "defaultModelsExpandDepth": -1},
)
