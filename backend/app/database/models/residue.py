from enum import Enum
from typing import TYPE_CHECKING, List
from decimal import Decimal

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import LayerResidue, HetResidue


class Residues(Enum):
    ALA = 1
    ARG = 2
    ASN = 3
    ASP = 4
    CYS = 5
    GLU = 6
    GLN = 7
    GLY = 8
    HIS = 9
    ILE = 10
    LEU = 11
    LYS = 12
    MET = 13
    PHE = 14
    PRO = 15
    SER = 16
    THR = 17
    TRP = 18
    TYR = 19
    VAL = 20


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
