"""Database models for protein structure sources.

This module defines SQLModel classes for storing and retrieving information about
the sources of protein structures, such as the Protein Data Bank (PDB) and AlphaFill.
"""

from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Structure


class Sources(Enum):
    """Enumeration of protein structure sources.

    This enum provides a mapping between source names and their corresponding
    numeric IDs used in the database.
    """

    PDB = 1
    ALPHAFILL = 2


class SourceBase(SQLModel):
    """Base model for source data.

    Attributes:
        name: Name of the source (e.g., 'PDB', 'AlphaFill').
    """

    name: str = Field(index=True)


class Source(SourceBase, table=True):
    """Database model for sources.

    Attributes:
        id: Primary key for the source.
        structures: Associated protein structures from this source.
    """

    id: int = Field(primary_key=True)

    structures: List["Structure"] = Relationship(back_populates="source")
