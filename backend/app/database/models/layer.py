from sqlmodel import Field, SQLModel, Relationship
from app.database.models import Channel, LayerResidue


class Layer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")
    order: int
    radius: float
    free_radius: float
    start_distance: float
    end_distance: float
    local_minimum: bool
    bottleneck: bool

    channel: Channel = Relationship(back_populates="layers")
    residues: list[LayerResidue] = Relationship(back_populates="layer")
