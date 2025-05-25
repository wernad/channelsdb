"""Database models for protein structures.

This module defines SQLModel classes for storing and retrieving protein structure data,
including their relationships with channels and sources, and versioning information.
"""

from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from app.database.models import Channel, Source


class StructureBase(SQLModel):
    """Base model for structure data.

    Attributes:
        has_channels: Whether the structure contains any channels.
        version: Version number of the structure.
    """

    has_channels: bool
    version: int = Field(nullable=True)


class StructureInsert(StructureBase):
    """Model for inserting new structures.

    Attributes:
        external_id: External identifier for the structure (e.g., PDB ID).
        source_id: Foreign key reference to the structure source.
    """

    external_id: str = Field(nullable=False)
    source_id: int = Field(foreign_key="source.id")


class Structure(StructureInsert, table=True):
    """Database model for structures.

    Attributes:
        id: Primary key for the structure.
        channels: Associated channels in this structure.
        source: Source of the structure.
    """

    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="structure")
    source: "Source" = Relationship(back_populates="structures")

    __table_args__ = (UniqueConstraint("external_id", "version"),)


class StructureData(SQLModel):
    """Model for structure data in API requests.

    Attributes:
        source_id: ID of the structure source.
        version: Version number of the structure.
    """

    source_id: int
    version: int


class StructurePagination(SQLModel):
    """Model for pagination limit and offset.

    Attributes:
        limit: number of entries to fetch.
        offset: number of entries to skip.
    """

    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=1000000)
    offset: int = Field(0, ge=0)
