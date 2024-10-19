from sqlmodel import Field, SQLModel


class Annotation(SQLModel, table=True):
    id: int = Field(primary_key=True)
    structure_id: int
    name: str
    description: str
    reference: str
    referenceType: str
