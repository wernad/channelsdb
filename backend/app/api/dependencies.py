from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database.database import get_session
from app.database.repositories import ChannelRepository

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_repo(db: Session = SessionDep) -> ChannelRepository:
    return ChannelRepository(db)


ChannelsRepositoryDep = Annotated[ChannelRepository, Depends(get_user_repo)]
