from typing import TYPE_CHECKING, List
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel, LayerResidue


class LayerBase(SQLModel):
    radius: Decimal = Field(decimal_places=3)
    free_radius: Decimal = Field(decimal_places=3)
    start_distance: Decimal = Field(decimal_places=3)
    end_distance: Decimal = Field(decimal_places=3)
    local_minimum: bool
    bottleneck: bool | None = Field(default=None)


class Layer(LayerBase, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")
    layer_order: int

    channel: "Channel" = Relationship(back_populates="layers")
    layer_residues: List["LayerResidue"] = Relationship(cascade_delete=True, back_populates="layer")


class LayerGeometry(LayerBase):
    pass


class LayerProperties(SQLModel):
    charge: int
    num_positives: int
    num_negatives: int
    hydrophobicity: float
    hydropathy: float
    polarity: float
    mutability: float


class LayerInfo(SQLModel):
    layer_geometry: LayerGeometry
    residues: list[str]
    properties: LayerProperties


class Layers(SQLModel):
    residue_flow: list[str]
    het_residues: list[str]
    layers_info: list[LayerInfo]
