from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel, LayerResidue


class LayerBase(SQLModel):
    channel_id: int = Field(unique=True, foreign_key="channel.id")
    order: int
    radius: float
    free_radius: float
    start_distance: float
    end_distance: float
    local_minimum: bool
    bottleneck: bool


class Layer(LayerBase, table=True):
    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="layers")
    residues: list["LayerResidue"] = Relationship(back_populates="layer")


class LayerOutput(LayerBase):
    pass
