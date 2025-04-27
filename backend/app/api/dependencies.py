from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Path
from sqlmodel import Session

from app.api.common import NEW_PDB_ID_REGEX, OLD_PDB_ID_REGEX, UNIPROT_ID_REGEX
from app.database.database import engine
from app.database.repositories import ChannelRepository
from app.services import (AnnotationService, ChannelService, ExportService,
                          StatisticsService, StructureService)

__all__ = [
    "AnnotationServiceDep",
    "ChannelServiceDep",
    "ExportServiceDep",
    "StructureServiceDep",
    "IDCheckDep",
]

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

# Statistics


def get_statistics_service(db: SessionDep) -> Generator[StatisticsService, None, None]:
    yield StatisticsService(db)


StatisticsServiceDep = Annotated[StatisticsService, Depends(get_statistics_service)]

# Statistics


def get_structure_service(db: SessionDep) -> Generator[StructureService, None, None]:
    yield StructureService(db)


StructureServiceDep = Annotated[StructureService, Depends(get_structure_service)]

# ID handling


def validate_id(
    structure_id: Annotated[
        str, Path(pattern=f"{OLD_PDB_ID_REGEX}|{NEW_PDB_ID_REGEX}|{UNIPROT_ID_REGEX}")
    ],
) -> str:
    """Validates passed identifier and if it is in old PDB format transforms it into the new format.

    Args:
        structure_id: id to validate
    Returns:
        Same or updated string id value.
    """

    if len(structure_id) == 4:
        structure_id = f"pdb_0000{structure_id}"

    return structure_id


IDCheckDep = Annotated[str, Depends(validate_id)]
