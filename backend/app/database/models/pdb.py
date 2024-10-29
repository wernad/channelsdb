from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from app.database.models import Channel, Annotation


class PDBDataBase(SQLModel):
    has_channels: bool


class PDBData(PDBDataBase, table=True):
    structure_id: str = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="structure")
    annotations: List["Annotation"] = Relationship(back_populates="structure")
