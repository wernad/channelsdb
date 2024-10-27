from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel, Residue


class HetResidueBase(SQLModel):
    sequence_number: int
    chain_id: str


class HetResidue(HetResidueBase, table=True):
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    channel_id: int = Field(primary_key=True, foreign_key="channel.id")

    residue: "Residue" = Relationship(back_populates="het_residues")
    channel: "Channel" = Relationship(back_populates="het_residues")


class HetResidueOutput(HetResidueBase):
    pass
