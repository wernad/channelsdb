from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.database.models import Channel, Annotation, Source


class StructureBase(SQLModel):
    has_channels: bool
    version: int = Field(nullable=True)


class Structure(StructureBase, table=True):
    id: str = Field(primary_key=True)
    source_id: int = Field(foreign_key="source.id")

    channels: List["Channel"] = Relationship(back_populates="structure")
    annotations: List["Annotation"] = Relationship(back_populates="structure")
    source: "Source" = Relationship(back_populates="structures")
