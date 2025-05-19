"""Database models for protein channel annotations."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class AnnotationBase(SQLModel):
    """Base model for channel annotations.

    Attributes:
        name: Name of the annotation.
        description: Detailed description of the annotation.
        reference: Reference information for the annotation.
        reference_type: Type of reference (e.g., publication, database).
    """

    name: str
    description: str
    reference: str
    reference_type: str


class AnnotationInsert(AnnotationBase):
    """Model for inserting new annotations.

    Attributes:
        channel_id: Foreign key reference to the associated channel.
    """

    channel_id: int = Field(foreign_key="channel.id")


class Annotation(AnnotationInsert, table=True):
    """Database model for channel annotations.

    Attributes:
        id: Primary key for the annotation.
        channel: Relationship to the associated channel.
    """

    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="annotations")


class AnnotationOutput(AnnotationBase):
    """Model for API responses containing annotation data.

    Attributes:
        id: Primary key of the annotation.
    """

    id: int


class ResidueAnnotationOutput(SQLModel):
    """Model for residue-specific annotation data in API responses.

    Attributes:
        channels_db: List of ChannelsDB annotations.
        uni_prot: List of UniProt annotations.
    """

    channels_db: list = Field(
        default_factory=list, schema_extra={"serialization_alias": "ChannelsDB"}
    )
    uni_prot: list = Field(
        default_factory=list, schema_extra={"serialization_alias": "UniProt"}
    )


class AnnotationsOutput(SQLModel):
    """Model for complete annotation data in API responses.

    Attributes:
        entry_annotations: List of entry-level annotations.
        residue_annotations: Residue-specific annotations.
    """

    entry_annotations: list[dict] = Field(
        default_factory=list, schema_extra={"serialization_alias": "EntryAnnotations"}
    )
    residue_annotations: ResidueAnnotationOutput = Field(
        default_factory=ResidueAnnotationOutput,
        schema_extra={"serialization_alias": "ResidueAnnotations"},
    )
