from decimal import Decimal
from typing import TYPE_CHECKING, Annotated, List

from pydantic import PlainSerializer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel, LayerResidue


class LayerBase(SQLModel):
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
    channel_id: int = Field(foreign_key="channel.id")
    layer_order: int


class Layer(LayerInsert, table=True):
    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="layers")
    layer_residues: List["LayerResidue"] = Relationship(
        cascade_delete=True, back_populates="layer"
    )


class LayerGeometry(LayerBase):
    pass


class LayerProperties(SQLModel):
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
    layer_geometry: LayerGeometry = Field(
        schema_extra={"serialization_alias": "LayerGeometry"}
    )
    residues: list[str] = Field(schema_extra={"serialization_alias": "Residues"})
    properties: LayerProperties = Field(
        schema_extra={"serialization_alias": "Properties"}
    )


class Layers(SQLModel):
    residue_flow: list[str] = Field(schema_extra={"serialization_alias": "ResidueFlow"})
    het_residues: list[str] = Field(schema_extra={"serialization_alias": "HeyResidues"})
    layers_info: list[LayerInfo] = Field(
        schema_extra={"serialization_alias": "LayersInfo"}
    )
