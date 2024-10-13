from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://postgres:admin@postgresserver/db"


connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
