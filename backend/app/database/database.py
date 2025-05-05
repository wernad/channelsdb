from contextlib import contextmanager
from os import environ, getpid
from time import sleep
from typing import Generator

from pydantic_core import MultiHostUrl
from sqlmodel import Session, SQLModel, create_engine, inspect, text

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.database.repositories import (
    CategoryRepository,
    MethodRepository,
    ResidueRepository,
    SourceRepository,
)
from app.log import log

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
    "structure",
    "source",
    "profile",
    "residue",
]


def check_if_tables_exist():
    inspector = inspect(engine)

    for table in REQUIRED_TABLES:
        if not inspector.has_table(table):
            return False

    return True


def create_db_and_tables():
    with engine.begin() as conn:
        log.debug(f"Create DB -- WORKER {getpid()} -- Attempting to acquire lock...")
        try:
            lock_id = "12345"
            lock_acquired = conn.execute(
                text(f"SELECT pg_try_advisory_lock({lock_id})")
            ).scalar()

            if lock_acquired:
                # Only this worker will perform the initialization
                log.debug(
                    f"Create DB -- WORKER {getpid()} -- Lock acquired, creating tables..."
                )
                # Your table creation code here
                SQLModel.metadata.create_all(bind=engine)

                # Release the lock when done
                conn.execute(text(f"SELECT pg_advisory_unlock({lock_id})"))
                log.debug(f"Create DB -- WORKER {getpid()} -- Tables created.")
            else:
                # Another worker is already creating tables, wait for completion.
                log.debug(
                    f"Create DB -- WORKER {getpid()} -- Waiting for tables to be created by another worker..."
                )
                while not check_if_tables_exist():
                    log.debug(f"Create DB -- WORKER {getpid()} - Waiting...")
                    sleep(5)

                log.debug(f"Create DB -- WORKER {getpid()} -- Done waiting")
        except Exception as e:
            log.debug(f"Error during table creation: {e}")


def init_flag_data():
    """Insert rows into tables with flag-like data (method, category, source)."""
    with db_context() as db:
        log.debug(f"Fill DB -- WORKER {getpid()} -- Attempting to acquire lock...")
        try:
            lock_id = "12345"
            lock_acquired = db.exec(
                text(f"SELECT pg_try_advisory_lock({lock_id})")
            ).scalar()

            if lock_acquired:
                log.debug(
                    f"Fill DB -- WORKER {getpid()} -- Lock acquired, inserting data..."
                )
                method_repo = MethodRepository(db)
                category_repo = CategoryRepository(db)
                source_repo = SourceRepository(db)
                residue_repo = ResidueRepository(db)

                method_repo.init_table()
                category_repo.init_table()
                source_repo.init_table()
                residue_repo.init_table()

            else:
                # Another worker is already inseting data, wait for completion.
                log.debug(
                    f"Fill DB -- WORKER {getpid()} -- Waiting for data to be inserted by another worker..."
                )
                while not check_if_tables_exist():
                    log.debug(f"Fill DB -- WORKER {getpid()} - Waiting...")
                    sleep(5)

                log.debug(f"Fill DB -- WORKER {getpid()} -- Done waiting")
        except Exception as e:
            log.debug(f"Fill DB -- Error during table data initialization: {e}")
