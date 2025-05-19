from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from psycopg2 import OperationalError
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.config import API_PATH
from app.database.database import create_db_and_tables, init_flag_data
from app.log import log
from app.channels.data.scheduler import get_scheduler

router = APIRouter()
router.include_router(api_router, prefix=API_PATH)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        init_flag_data()
    except OperationalError as e:
        log.error(f"An operational error occured white creating tables: {e.pgcode}")
    scheduler = get_scheduler()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title="ChannelsDB 2.1 API",
    contact={"name": "Tomáš Raček", "email": "tomas.racek@ceitec.muni.cz"},
    redoc_url=None,
    docs_url="/",
    version="beta",
    swagger_ui_parameters={"syntaxHighlight": False, "defaultModelsExpandDepth": -1},
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
