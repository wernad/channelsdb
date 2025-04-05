from typing import TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from app.database.models import (
        Annotation,
        Method,
        Category,
        Layer,
        Layers,
        HetResidue,
        Profile,
        ProfileOutput,
        Structure,
    )


class ChannelBase(SQLModel):
    auto: bool
    cavity: int


class Channel(ChannelBase, table=True):
    id: int = Field(primary_key=True)
    structure_id: str = Field(foreign_key="structure.id")
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")

    annotation: "Annotation" = Relationship(back_populates="channel")
    structure: "Structure" = Relationship(back_populates="channels")
    method: "Method" = Relationship(back_populates="channels")
    category: "Category" = Relationship(back_populates="channels")
    layers: List["Layer"] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: List["HetResidue"] = Relationship(
        cascade_delete=True, back_populates="channel"
    )
    profiles: List["Profile"] = Relationship(back_populates="channel")


class ChannelOutput(ChannelBase):
    id: int
    type: str
    profile: list["ProfileOutput"]
    layers: "Layers"
