from contextlib import contextmanager
from os import environ, getpid

from time import sleep
from typing import Generator

from sqlmodel import Session, create_engine, SQLModel, text, inspect
from pydantic_core import MultiHostUrl

from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from app.log import logger as log

__all__ = ["db_context", "create_db_and_tables", "get_session"]

DATABASE_URL = str(
    MultiHostUrl.build(
        scheme="postgresql",
        username=environ.get("POSTGRES_USER", DB_USER),
        password=environ.get("POSTGRES_PASSWORD", DB_PASSWORD),
        host=environ.get("POSTGRES_HOST", DB_HOST),
        port=int(port) if (port := environ.get("POSTGRES_PORT", None)) else DB_PORT,
        path=environ.get("POSTGRES_NAME", DB_NAME),
    )
)


engine = create_engine(DATABASE_URL)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


db_context = contextmanager(get_session)

REQUIRED_TABLES = [
    "annotation",
    "category",
    "channel",
    "configfile",
    "hetresidue",
    "layerresidue",
    "layer",
    "layerresidue",
    "method",
    "pdbdata",
    "profile",
    "residue",
]


def check_if_tables_exist():
    inspector = inspect(engine)

    for table in REQUIRED_TABLES:
        # log.debug(f"WORKER {getpid()} -- {table} -- {inspector.has_table(table)}")
        if not inspector.has_table(table):
            return False

    return True


def create_db_and_tables():
    with engine.begin() as conn:
        log.debug(f"WORKER {getpid()} -- Attempting to acquire lock...")
        try:
            lock_acquired = conn.execute(
                text("SELECT pg_try_advisory_lock(12345)")
            ).scalar()

            if lock_acquired:
                # Only this worker will perform the initialization
                log.debug(f"WORKER {getpid()} -- Lock acquired, creating tables...")
                # Your table creation code here
                SQLModel.metadata.create_all(bind=engine)

                # Release the lock when done
                conn.execute(text("SELECT pg_advisory_unlock(12345)"))
                log.debug(f"WORKER {getpid()} -- Tables created.")
            else:
                # Another worker is already creating tables, wait for completion
                log.debug(
                    f"WORKER {getpid()} -- Waiting for tables to be created by another worker..."
                )
                while not check_if_tables_exist():
                    log.debug(f"WORKER {getpid()} - Waiting...")
                    sleep(5)

                log.debug(f"WORKER {getpid()} -- Done waiting")
        except Exception as e:
            log.debug(f"Error during initialization: {e}")
