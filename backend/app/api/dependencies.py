from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.database.database import engine
from app.database.repositories import ChannelRepository
from app.services import AnnotationService, ChannelService, ExportService
from app.api.exceptions import UnsupportedIDFormat

__all__ = [
    "AnnotationServiceDep",
    "ChannelServiceDep",
    "ExportServiceDep",
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

# ID handling


def check_protein_id(protein_id: str):
    if len(protein_id) == 4:  # Old PDB ID
        protein_id = f"pdb_0000{protein_id}"
    elif len(protein_id) == 12 and protein_id.startswith("pdb_"):  # New PDB id
        pass
    elif len(protein_id) == 6 and protein_id.startswith("P"):  # UniProt ID
        pass
    else:
        raise UnsupportedIDFormat(protein_id=protein_id)

    return protein_id


IDCheckDep = Annotated[str, Depends(check_protein_id)]
