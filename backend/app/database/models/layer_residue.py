from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Layer, Residue


class LayerResidueBase(SQLModel):
    sequence_number: int
    chain_id: str
    flow_id: int
    backbone: bool


class LayerResidueInsert(LayerResidueBase):
    layer_id: int = Field(foreign_key="layer.id")
    residue_id: int | None = Field(foreign_key="residue.id", nullable=True)


class LayerResidue(LayerResidueInsert, table=True):
    id: int = Field(primary_key=True)

    layer: "Layer" = Relationship(back_populates="layer_residues")
    residue: "Residue" = Relationship(back_populates="layer_residues")


class LayerResidueOutput(LayerResidueBase):
    pass
