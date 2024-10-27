from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models.pdb import PDBData


class AnnotationBase(SQLModel):
    structure_id: str = Field(foreign_key="pdbdata.structure_id")
    name: str
    description: str
    reference: str
    reference_type: str


class Annotation(AnnotationBase, table=True):
    id: int = Field(primary_key=True)

    structure: "PDBData" = Relationship(back_populates="structure")


class AnnotationOutput(AnnotationBase):
    pass
