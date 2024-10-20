from typing import TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Method, Category, Layer, HetResidue, ProfileOutput


class ChannelBase(SQLModel):
    structure_id: int
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")
    auto: bool
    cavity: int


class Channel(ChannelBase, table=True):
    id: int = Field(primary_key=True)

    method: "Method" = Relationship(back_populates="channels")
    category: "Category" = Relationship(back_populates="channels")
    layers: list["Layer"] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: list["HetResidue"] = Relationship(back_populates="channel")


class ChannelOutput(ChannelBase):
    profiles: List["ProfileOutput"]


class Channels(SQLModel):
    channels: List["Channel"]
