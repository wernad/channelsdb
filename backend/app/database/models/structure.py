from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from app.database.models import Channel, Source


class StructureBase(SQLModel):
    has_channels: bool
    version: int = Field(nullable=True)


class StructureInsert(StructureBase):
    external_id: str = Field(nullable=False)
    source_id: int = Field(foreign_key="source.id")


class Structure(StructureInsert, table=True):
    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="structure")
    source: "Source" = Relationship(back_populates="structures")

    __table_args__ = (UniqueConstraint("external_id", "version"),)


class StructureData(SQLModel):
    source_id: int
    version: int
