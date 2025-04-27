from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel, Residue


class HetResidueBase(SQLModel):
    sequence_number: int
    chain_id: str
    backbone: bool


class HetResidueInsert(HetResidueBase):
    residue_id: int | None = Field(foreign_key="residue.id", nullable=True)
    channel_id: int = Field(foreign_key="channel.id")


class HetResidue(HetResidueInsert, table=True):
    id: int = Field(primary_key=True)

    residue: "Residue" = Relationship(back_populates="het_residues")
    channel: "Channel" = Relationship(back_populates="het_residues")


class HetResidueOutput(HetResidueBase):
    pass
