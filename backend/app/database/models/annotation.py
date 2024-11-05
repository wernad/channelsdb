from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.database.models import PDBData, Channel


class AnnotationBase(SQLModel):
    structure_id: str = Field(foreign_key="pdbdata.structure_id")
    channel_id: int = Field(foreign_key="channel.id")
    name: str
    description: str
    reference: str
    reference_type: str


class Annotation(AnnotationBase, table=True):
    id: int = Field(primary_key=True)

    structure: "PDBData" = Relationship(back_populates="annotations")
    channel: "Channel" = Relationship(back_populates="annotation")


class AnnotationOutput(AnnotationBase):
    pass
