from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database.database import engine
from app.database.repositories import ChannelRepository


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_channel_repo(
    db: SessionDep,
) -> Generator[ChannelRepository, None, None]:
    yield ChannelRepository(db)


ChannelsRepositoryDep = Annotated[ChannelRepository, Depends(get_channel_repo)]
