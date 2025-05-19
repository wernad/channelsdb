"""Database models for channel layers.

Layers represent parts of channel with their own characteristics
based on their residues.
"""

from decimal import Decimal
from typing import TYPE_CHECKING, Annotated, List

from pydantic import PlainSerializer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel, LayerResidue


class LayerBase(SQLModel):
    """Base model for channel layer data.

    Attributes:
        radius: Radius of the layer.
        free_radius: Free radius of the layer.
        start_distance: Distance from channel start.
        end_distance: Distance from channel end.
        local_minimum: Whether this is a local minimum.
        bottleneck: Whether this is a bottleneck point.
    """

    radius: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "Radius"})
    free_radius: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "FreeRadius"})
    start_distance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "StartDistance"})
    end_distance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "EndDistance"})
    local_minimum: bool = Field(schema_extra={"serialization_alias": "LocalMinimum"})
    bottleneck: bool | None = Field(
        default=None, schema_extra={"serialization_alias": "Bottleneck"}
    )


class LayerInsert(LayerBase):
    """Model for inserting new layers.

    Attributes:
        channel_id: Foreign key reference to the associated channel.
        layer_order: Order of the layer in the channel sequence.
    """

    channel_id: int = Field(foreign_key="channel.id")
    layer_order: int


class Layer(LayerInsert, table=True):
    """Database model for channel layers.

    Attributes:
        id: Primary key for the layer.
        channel: Associated channel.
        layer_residues: Residues within this layer.
    """

    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="layers")
    layer_residues: List["LayerResidue"] = Relationship(
        cascade_delete=True, back_populates="layer"
    )


class LayerGeometry(LayerBase):
    """Model for layer geometric properties."""


class LayerProperties(SQLModel):
    """Model for layer chemical and physical properties.

    Attributes:
        charge: Net charge of the layer.
        num_positives: Number of positive residues.
        num_negatives: Number of negative residues.
        hydrophobicity: Hydrophobicity score.
        hydropathy: Hydropathy score.
        polarity: Polarity score.
        mutability: Mutability score.
    """

    charge: int = Field(schema_extra={"serialization_alias": "Charge"})
    num_positives: int = Field(schema_extra={"serialization_alias": "NumPositives"})
    num_negatives: int = Field(schema_extra={"serialization_alias": "NumNegatives"})
    hydrophobicity: float = Field(
        schema_extra={"serialization_alias": "Hydrophobicity"}
    )
    hydropathy: float = Field(schema_extra={"serialization_alias": "Hydropathy"})
    polarity: float = Field(schema_extra={"serialization_alias": "Polarity"})
    mutability: float = Field(schema_extra={"serialization_alias": "Mutability"})


class LayerInfo(SQLModel):
    """Model for complete layer information in API responses.

    Attributes:
        layer_geometry: Geometric properties of the layer.
        residues: List of residue identifiers in the layer.
        properties: Chemical and physical properties of the layer.
    """

    layer_geometry: LayerGeometry = Field(
        schema_extra={"serialization_alias": "LayerGeometry"}
    )
    residues: list[str] = Field(schema_extra={"serialization_alias": "Residues"})
    properties: LayerProperties = Field(
        schema_extra={"serialization_alias": "Properties"}
    )


class Layers(SQLModel):
    """Model for complete channel layer data in API responses.

    Attributes:
        residue_flow: List of residue identifiers in the channel.
        het_residues: List of het residue identifiers.
        layers_info: List of detailed layer information.
    """

    residue_flow: list[str] = Field(schema_extra={"serialization_alias": "ResidueFlow"})
    het_residues: list[str] = Field(schema_extra={"serialization_alias": "HetResidues"})
    layers_info: list[LayerInfo] = Field(
        schema_extra={"serialization_alias": "LayersInfo"}
    )
