from typing import TYPE_CHECKING
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel, Residue


class HetResidueBase(SQLModel):
    sequence_number: int
    chain_id: str
    backbone: bool


class HetResidue(HetResidueBase, table=True):
    id: int = Field(primary_key=True)
    residue_id: int = Field(foreign_key="residue.id")
    channel_id: int = Field(foreign_key="channel.id")

    residue: "Residue" = Relationship(back_populates="het_residues")
    channel: "Channel" = Relationship(back_populates="het_residues")

    __table_args__ = (
        UniqueConstraint(
            "channel_id", "residue_id", "sequence_number", "chain_id", "backbone"
        ),
    )


class HetResidueOutput(HetResidueBase):
    pass
