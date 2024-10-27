from typing import TYPE_CHECKING
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Layer, Residue


class LayerResidueBase(SQLModel):
    sequence_number: int
    chain_id: str
    flow_id: int
    coord_x: Decimal = Field(decimal_places=3)
    coord_y: Decimal = Field(decimal_places=3)
    coord_z: Decimal = Field(decimal_places=3)
    backbone: bool


class LayerResidue(LayerResidueBase, table=True):
    layer_id: int = Field(primary_key=True, foreign_key="layer.id")
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")

    layer: "Layer" = Relationship(back_populates="layer_residues")
    residue: "Residue" = Relationship(back_populates="layer_residues")


class LayerResidueOutput(LayerResidueBase):
    pass
