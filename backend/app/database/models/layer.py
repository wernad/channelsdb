from typing import TYPE_CHECKING
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel, LayerResidue


class LayerBase(SQLModel):
    channel_id: int = Field(unique=True, foreign_key="channel.id")
    order: int
    radius: Decimal = Field(decimal_places=3)
    free_radius: Decimal = Field(decimal_places=3)
    start_distance: Decimal = Field(decimal_places=3)
    end_distance: Decimal = Field(decimal_places=3)
    local_minimum: bool
    bottleneck: bool


class Layer(LayerBase, table=True):
    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="layers")
    residues: list["LayerResidue"] = Relationship(back_populates="layer")


class LayerOutput(LayerBase):
    pass
