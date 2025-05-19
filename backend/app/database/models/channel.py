"""Database models for protein channels.

Channels represent tunnels, pores, and other pathways in protein structures.
"""

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
    """Base model for channel data.

    Attributes:
        auto: Whether the channel was automatically detected.
        cavity: Cavity identifier associated with the channel.
        type: Type of channel (e.g., tunnel, pore).
    """

    auto: bool = Field(schema_extra={"serialization_alias": "Auto"})
    cavity: str = Field(schema_extra={"serialization_alias": "Cavity"})
    type: str = Field(nullable=False, schema_extra={"serialization_alias": "Type"})


class ChannelInsert(ChannelBase):
    """Model for inserting new channels.

    Attributes:
        structure_id: Foreign key reference to the associated structure.
        method_id: Foreign key reference to the calculation method used.
    """

    structure_id: int = Field(foreign_key="structure.id")
    method_id: int = Field(foreign_key="method.id")


class Channel(ChannelInsert, table=True):
    """Database model for channels.

    Attributes:
        id: Primary key for the channel.
        annotations: Related annotations for this channel.
        structure: Associated protein structure.
        method: Detection method used.
        layers: Channel layers.
        het_residues: Het residues in the channel.
        profiles: Channel profiles (physical structure)
    """

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
    """Model for channel data in API responses.

    Attributes:
        id: Channel identifier.
        profile: List of channel profiles.
        layers: Channel layers data.
    """

    id: str = Field(schema_extra={"serialization_alias": "Id"})
    profile: list["ProfileOutput"] = Field(
        schema_extra={"serialization_alias": "Profile"}
    )
    layers: "Layers" = Field(schema_extra={"serialization_alias": "Layers"})


class ChannelsResponse(SQLModel):
    """Model for complete channel data in API responses.

    Attributes:
        annotations: List of channel annotations.
        channels: Dictionary mapping channel types to lists of channels.
    """

    annotations: List["AnnotationOutput"] = Field(
        schema_extra={"serialization_alias": "Annotations"}, default_factory=list
    )
    channels: Dict[str, List[ChannelOutput]] = Field(
        schema_extra={"serialization_alias": "Channels"}
    )


class ChannelFilter(SQLModel):
    """Model for filtering channel queries.

    Attributes:
        min_radius: Minimum channel radius.
        max_radius: Maximum channel radius.
        min_distance: Minimum channel distance.
        max_distance: Maximum channel distance.
        min_bottleneck: Minimum bottleneck in layer radius.
        limit: Maximum number of results to return.
        offset: Number of results to skip.
    """

    model_config = {"extra": "forbid"}

    min_radius: float | None = Field(None, ge=0)
    max_radius: float | None = Field(None, ge=0)
    min_distance: float | None = Field(None, ge=0)
    max_distance: float | None = Field(None, ge=0)
    min_bottleneck: float | None = Field(None, ge=0)

    limit: int = Field(100, gt=0, le=1000000)
    offset: int = Field(0, ge=0)
