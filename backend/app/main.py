from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from starlette.requests import Request

from app.config import API_PATH
from app.api.main import api_router
from app.database.database import create_db_and_tables
from psycopg2 import OperationalError
from app.log import logger as log

router = APIRouter()
router.include_router(api_router, prefix=API_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        log.debug("Creating database and tables.")
        create_db_and_tables()
        log.debug("Database and tables created successfully.")
    except OperationalError as e:
        log.error(f"An operational error occured white creating tables: {e.pgcode}")

    yield


app = FastAPI(
    title="ChannelsDB 2.1 API",
    contact={"name": "Tomáš Raček", "email": "tomas.racek@ceitec.muni.cz"},
    redoc_url=None,
    docs_url="/",
    version="beta",
    swagger_ui_parameters={"syntaxHighlight": False, "defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)

app.include_router(router)
