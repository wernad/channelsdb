from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel


class HetResidueBase(SQLModel):
    sequence_number: int
    type: str


class HetResidue(HetResidueBase, table=True):
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    channel_id: int = Field(primary_key=True, foreign_key="channel.id")

    channel: "Channel" = Relationship(back_populates="channel")


class HetResidueOutput(HetResidueBase):
    pass
