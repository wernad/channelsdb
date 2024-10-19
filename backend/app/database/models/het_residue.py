from sqlmodel import Field, SQLModel, Relationship
from app.database.models import Channel


class HetResidue(SQLModel, table=True):
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    channel_id: int = Field(primary_key=True, foreign_key="channel.id")
    sequence_number: int
    type: str

    channel: Channel = Relationship(back_populates="channel")
