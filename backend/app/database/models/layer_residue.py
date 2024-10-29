from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint

if TYPE_CHECKING:
    from app.database.models import Layer, Residue


class LayerResidueBase(SQLModel):
    sequence_number: int
    chain_id: str
    flow_id: int
    backbone: bool


class LayerResidue(LayerResidueBase, table=True):
    id: int = Field(primary_key=True)
    layer_id: int = Field(foreign_key="layer.id")
    residue_id: int = Field(foreign_key="residue.id")

    layer: "Layer" = Relationship(back_populates="layer_residues")
    residue: "Residue" = Relationship(back_populates="layer_residues")

    __table_args__ = (
        UniqueConstraint(
            "layer_id", "residue_id", "sequence_number", "chain_id", "backbone"
        ),
    )


class LayerResidueOutput(LayerResidueBase):
    pass
