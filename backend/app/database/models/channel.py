from typing import TYPE_CHECKING, Dict, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import (
        Annotation,
        AnnotationOutput,
        HetResidue,
        Layer,
        Layers,
        Method,
        Profile,
        ProfileOutput,
        Structure,
    )


class ChannelBase(SQLModel):
    auto: bool = Field(schema_extra={"serialization_alias": "Auto"})
    cavity: str = Field(schema_extra={"serialization_alias": "Cavity"})
    type: str = Field(nullable=False, schema_extra={"serialization_alias": "Type"})


class ChannelInsert(ChannelBase):
    structure_id: int = Field(foreign_key="structure.id")
    method_id: int = Field(foreign_key="method.id")


class Channel(ChannelInsert, table=True):
    id: int = Field(primary_key=True)

    annotations: list["Annotation"] = Relationship(back_populates="channel")
    structure: "Structure" = Relationship(back_populates="channels")
    method: "Method" = Relationship(back_populates="channels")
    layers: List["Layer"] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: List["HetResidue"] = Relationship(
        cascade_delete=True, back_populates="channel"
    )
    profiles: List["Profile"] = Relationship(back_populates="channel")


class ChannelOutput(ChannelBase):
    id: str = Field(schema_extra={"serialization_alias": "Id"})
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


class ChannelFilter(SQLModel):
    model_config = {"extra": "forbid"}

    min_radius: float | None = Field(None, ge=0)
    max_radius: float | None = Field(None, ge=0)
    min_distance: float | None = Field(None, ge=0)
    max_distance: float | None = Field(None, ge=0)
    min_bottleneck: float | None = Field(None, ge=0)

    limit: int = Field(100, gt=0, le=1000000)
    offset: int = Field(0, ge=0)
