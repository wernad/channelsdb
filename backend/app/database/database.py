from sqlmodel import create_engine, SQLModel
from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME, DB_PORT
from pydantic_core import MultiHostUrl
from os import environ

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


engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)
