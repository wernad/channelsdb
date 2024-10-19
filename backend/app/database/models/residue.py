from sqlmodel import Field, SQLModel, Relationship
from app.database.models import LayerResidue


class Residue(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    charge: int = Field(index=True)
    hodropathy: float = Field(index=True)
    polarity: float = Field(index=True)
    mutability: int = Field(index=True)

    layers: list[LayerResidue] = Relationship(back_populates="residue")
