from typing import TYPE_CHECKING, Dict, List

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
        AnnotationOutput,
    )


class ChannelBase(SQLModel):
    auto: bool = Field(schema_extra={"serialization_alias": "Auto"})
    cavity: str = Field(schema_extra={"serialization_alias": "Cavity"})


class Channel(ChannelBase, table=True):
    id: int = Field(primary_key=True)
    structure_id: int = Field(foreign_key="structure.id")
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
    id: str = Field(schema_extra={"serialization_alias": "Id"})
    type: str = Field(schema_extra={"serialization_alias": "Type"})
    profile: list["ProfileOutput"] = Field(
        schema_extra={"serialization_alias": "Profile"}
    )
    layers: "Layers" = Field(schema_extra={"serialization_alias": "Layers"})


class ChannelsResponse(SQLModel):
    annotations: List["AnnotationOutput"] = Field(
        schema_extra={"serialization_alias": "Annotations"}, default_factory=list
    )
    channels: Dict[str, List[ChannelOutput]] = Field(
        schema_extra={"serialization_alias": "Channels"}
    )
