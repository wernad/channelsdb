from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Layer, Residue


class LayerResidueBase(SQLModel):
    sequence_number: int
    type: str
    flow_id: int
    coord_x: float
    coord_y: float
    coord_z: float
    backbone: bool


class LayerResidue(LayerResidueBase, table=True):
    layer_id: int = Field(primary_key=True, foreign_key="layers.id")
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")

    layer: "Layer" = Relationship(back_populates="residues")
    residue: "Residue" = Relationship(back_populates="layers")


class LayerResidueOutput(LayerResidueBase):
    pass
