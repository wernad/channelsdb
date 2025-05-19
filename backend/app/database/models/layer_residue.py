"""Database models for connecting residues to layers."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Layer, Residue


class LayerResidueBase(SQLModel):
    """Base model for layer residue data.

    Attributes:
        sequence_number: Position in the protein sequence.
        chain_id: Identifier of the protein chain.
        flow_id: Order of residue in the layer.
        backbone: Whether the residue is part of the backbone.
    """

    sequence_number: int
    chain_id: str
    flow_id: int
    backbone: bool


class LayerResidueInsert(LayerResidueBase):
    """Model for inserting new layer residues.

    Attributes:
        layer_id: Foreign key reference to the associated layer.
        residue_id: Optional foreign key reference to the residue.
    """

    layer_id: int = Field(foreign_key="layer.id")
    residue_id: int | None = Field(foreign_key="residue.id", nullable=True)


class LayerResidue(LayerResidueInsert, table=True):
    """Database model for layer residues.

    Attributes:
        id: Primary key for the layer residue.
        layer: Associated layer.
        residue: Related residue if applicable.
    """

    id: int = Field(primary_key=True)

    layer: "Layer" = Relationship(back_populates="layer_residues")
    residue: "Residue" = Relationship(back_populates="layer_residues")


class LayerResidueOutput(LayerResidueBase):
    """Model for layer residue data in API responses."""

    pass
