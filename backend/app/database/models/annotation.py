from sqlmodel import Field, SQLModel


class AnnotationBase(SQLModel):
    structure_id: int
    name: str
    description: str
    reference: str
    reference_type: str


class Annotation(AnnotationBase, table=True):
    id: int = Field(primary_key=True)


class AnnotationOutput(AnnotationBase):
    pass
