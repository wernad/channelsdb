from sqlmodel import Field, SQLModel, Relationship
from app.database.models import Layer, Residue


class LayerResidue(SQLModel, table=True):
    layer_id: int = Field(primary_key=True, foreign_key="layers.id")
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    sequence_number: int
    type: str
    flow_id: int
    coord_x: float
    coord_y: float
    coord_z: float
    backbone: bool

    layer: Layer = Relationship(back_populates="residues")
    residue: Residue = Relationship(back_populates="layers")
