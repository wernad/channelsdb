"""Database models for het residues in protein channels."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel, Residue


class HetResidueBase(SQLModel):
    """Base model for het residue data.

    Attributes:
        sequence_number: Position in the protein sequence.
        chain_id: Identifier of the protein chain.
        backbone: Whether the residue is part of the backbone.
    """

    sequence_number: int
    chain_id: str
    backbone: bool


class HetResidueInsert(HetResidueBase):
    """Model for inserting new het residues.

    Attributes:
        residue_id: Optional foreign key reference to the residue.
        channel_id: Foreign key reference to the associated channel.
    """

    residue_id: int | None = Field(foreign_key="residue.id", nullable=True)
    channel_id: int = Field(foreign_key="channel.id")


class HetResidue(HetResidueInsert, table=True):
    """Database model for het residues.

    Attributes:
        id: Primary key for the het residue.
        residue: Related residue if applicable.
        channel: Associated channel.
    """

    id: int = Field(primary_key=True)

    residue: "Residue" = Relationship(back_populates="het_residues")
    channel: "Channel" = Relationship(back_populates="het_residues")


class HetResidueOutput(HetResidueBase):
    """Model for het residue data in API responses."""

    pass
