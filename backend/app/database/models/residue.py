from typing import TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import LayerResidue


class ResidueBase(SQLModel):
    name: str
    charge: int = Field(index=True)
    hodropathy: float = Field(index=True)
    polarity: float = Field(index=True)
    mutability: int = Field(index=True)


class Residue(ResidueBase, table=True):
    id: int = Field(primary_key=True)

    layers: list["LayerResidue"] = Relationship(back_populates="residue")


class ResidueOutput(ResidueBase):
    pass
