"""Database module providing database connection and session management.

Provides functionality for creating and initializing the database
with initializes flag-like data (method, source, residue) into the database.
"""

from contextlib import contextmanager
from os import environ, getpid
from time import sleep
from typing import Generator

from pydantic_core import MultiHostUrl
from sqlmodel import Session, SQLModel, create_engine, inspect, text

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.database.repositories import (
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
    """Creates and yields a database session.

    Returns:
        Generator yielding a SQLModel Session object.
    """
    with Session(engine) as session:
        yield session


db_context = contextmanager(get_session)

REQUIRED_TABLES = [
    "annotation",
    "channel",
    "hetresidue",
    "layer",
    "layerresidue",
    "method",
    "profile",
    "residue",
    "source",
    "structure",
]


def check_if_tables_exist():
    """Checks if all required database tables exist.

    Returns:
        bool: True if all required tables exist, False otherwise.
    """
    inspector = inspect(engine)

    for table in REQUIRED_TABLES:
        if not inspector.has_table(table):
            return False

    return True


def create_db_and_tables():
    """Creates all required database tables if they don't exist.

    Uses advisory locking to ensure only one process creates the tables
    while others wait for completion. Implements waiting mechanism for
    concurrent initialization scenarios.
    """
    with db_context() as db:
        log.debug(f"Create DB -- WORKER {getpid()} -- Attempting to acquire lock...")
        try:
            lock_id = "12345"
            lock_acquired = db.exec(
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
                db.exec(text(f"SELECT pg_advisory_unlock({lock_id})"))
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
    """Initializes flag-like data in the database.

    Inserts initial data into method, source, and residue tables.
    Uses advisory locking to ensure only one process performs the initialization
    while others wait for completion.
    """
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
                source_repo = SourceRepository(db)
                residue_repo = ResidueRepository(db)

                method_repo.init_table()
                source_repo.init_table()
                residue_repo.init_table()
                db.exec(text(f"SELECT pg_advisory_unlock({lock_id})"))
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
