from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database.database import engine
from app.api.services import AnnotationService, ChannelService

__all__ = ["AnnotationServiceDep", "ChannelServiceDep"]


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def get_channel_service(
    db: SessionDep,
) -> Generator[ChannelService, None, None]:
    yield ChannelService(db)


ChannelServiceDep = Annotated[ChannelService, Depends(get_channel_service)]


def get_annotation_service(db: SessionDep) -> Generator[AnnotationService, None, None]:
    yield AnnotationService(db)


AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]
