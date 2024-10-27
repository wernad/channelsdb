from typing import TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import (
        Method,
        Category,
        Layer,
        HetResidue,
        Profile,
        ProfileOutput,
        PDBData,
    )


class ChannelBase(SQLModel):
    structure_id: str = Field(foreign_key="pdbdata.structure_id")
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")
    auto: bool
    cavity: int


class Channel(ChannelBase, table=True):
    id: int = Field(primary_key=True)

    structure: "PDBData" = Relationship(back_populates="channels")
    method: "Method" = Relationship(back_populates="channels")
    category: "Category" = Relationship(back_populates="channels")
    layers: List["Layer"] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: List["HetResidue"] = Relationship(
        cascade_delete=True, back_populates="channel"
    )
    profiles: List["Profile"] = Relationship(back_populates="channel")


class ChannelOutput(ChannelBase):
    profiles: List["ProfileOutput"]


class Channels(SQLModel):
    channels: List["Channel"]
