from fastapi import FastAPI, APIRouter
from app.api.main import api_router
from app.config import API_PATH
from app.database.database import create_db_and_tables


router = APIRouter()
router.include_router(api_router, prefix=API_PATH)


app = FastAPI(
    title="ChannelsDB 2.1 API",
    contact={"name": "Tomáš Raček", "email": "tomas.racek@ceitec.muni.cz"},
    redoc_url=None,
    docs_url="/",
    version="beta",
    swagger_ui_parameters={"syntaxHighlight": False, "defaultModelsExpandDepth": -1},
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
