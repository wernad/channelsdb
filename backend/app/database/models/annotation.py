from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.database.models import Structure, Channel


class AnnotationBase(SQLModel):
    name: str
    description: str
    reference: str
    reference_type: str


class Annotation(AnnotationBase, table=True):
    id: int = Field(primary_key=True)
    structure_id: str = Field(foreign_key="structure.id")
    channel_id: int = Field(foreign_key="channel.id")

    structure: "Structure" = Relationship(back_populates="annotations")
    channel: "Channel" = Relationship(back_populates="annotation")


class AnnotationOutput(AnnotationBase):
    id: int


class ResidueAnnotationOutput(SQLModel):
    channels_db: list = Field(default_factory=list, alias="ChannelsDB")
    uni_prot: list = Field(default_factory=list, alias="UniProt")


class AnnotationsOutput(SQLModel):
    entry_annotations: list[dict] = Field(
        default_factory=list, alias="EntryAnnotations"
    )
    residue_annotations: ResidueAnnotationOutput = Field(
        default_factory=ResidueAnnotationOutput, alias="ResidueAnnotations"
    )
