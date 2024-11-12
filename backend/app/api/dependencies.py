from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database.database import engine
from app.database.repositories import ChannelRepository
from app.services import AnnotationService, ChannelService, ExportService

__all__ = ["AnnotationServiceDep", "ChannelServiceDep"]

# Session


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# Annotation


def get_annotation_service(db: SessionDep) -> Generator[AnnotationService, None, None]:
    yield AnnotationService(db)


AnnotationServiceDep = Annotated[AnnotationService, Depends(get_annotation_service)]

# Channel


def get_channel_repository(db: Session) -> Generator[ChannelRepository, None, None]:
    yield ChannelRepository(db)


ChannelRepositoryDep = Annotated[ChannelRepository, Depends(get_channel_repository)]


def get_channel_service(db: SessionDep) -> Generator[ChannelService, None, None]:
    yield ChannelService(db)


ChannelServiceDep = Annotated[ChannelService, Depends(get_channel_service)]

# Export


def get_export_service(db: SessionDep) -> Generator[ExportService, None, None]:
    yield ExportService(db)


ExportServiceDep = Annotated[ExportService, Depends(get_export_service)]
