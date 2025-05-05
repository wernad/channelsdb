from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class AnnotationBase(SQLModel):
    name: str
    description: str
    reference: str
    reference_type: str


class AnnotationInsert(AnnotationBase):
    channel_id: int = Field(foreign_key="channel.id")


class Annotation(AnnotationInsert, table=True):
    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="annotations")


class AnnotationOutput(AnnotationBase):
    id: int


class ResidueAnnotationOutput(SQLModel):
    channels_db: list = Field(
        default_factory=list, schema_extra={"serialization_alias": "ChannelsDB"}
    )
    uni_prot: list = Field(
        default_factory=list, schema_extra={"serialization_alias": "UniProt"}
    )


class AnnotationsOutput(SQLModel):
    entry_annotations: list[dict] = Field(
        default_factory=list, schema_extra={"serialization_alias": "EntryAnnotations"}
    )
    residue_annotations: ResidueAnnotationOutput = Field(
        default_factory=ResidueAnnotationOutput,
        schema_extra={"serialization_alias": "ResidueAnnotations"},
    )
