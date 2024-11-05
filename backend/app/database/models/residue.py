from typing import TYPE_CHECKING, List
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import LayerResidue, HetResidue


class ResidueBase(SQLModel):
    name: str
    charge: int | None = Field(index=True, default=None)
    hydropathy: Decimal | None = Field(index=True, decimal_places=3, default=None)
    hydrophobicity: Decimal | None = Field(index=True, decimal_places=3, default=None)
    polarity: Decimal | None = Field(index=True, decimal_places=3, default=None)
    mutability: int | None = Field(index=True, default=None)


class Residue(ResidueBase, table=True):
    id: int = Field(primary_key=True)

    layer_residues: List["LayerResidue"] = Relationship(back_populates="residue")
    het_residues: List["HetResidue"] = Relationship(back_populates="residue")


class ResidueOutput(ResidueBase):
    pass
