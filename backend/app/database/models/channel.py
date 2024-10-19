from sqlmodel import Field, SQLModel, Relationship

from app.database.models import Method, Category, Layer, HetResidue


class Channel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    structure_id: int
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")
    auto: bool

    method: Method = Relationship(back_populates="channels")
    category: Category = Relationship(back_populates="channels")
    layers: list[Layer] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: list[HetResidue] = Relationship(back_populates="channel")
