from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class Categories(Enum):
    CHANNEL = 1
    TUNNEL = 2
    PORE = 3
    SOLVENT_TUNNEL = 4
    SUBSTRATE_TUNNEL = 5
    SUBSTRATE_PRODUCT_TUNNEL = 6
    PRODUCT_TUNNEL = 7
    WATER_CHANNEL = 8
    ION_CHANNEL = 9
    HYDROPHOBIC_CHANNEL = 10
    PEPTIDE_CHANNEL = 11
    NUCLEOTIDE_CHANNEL = 12


CATEGORIES_ID_TO_NAME = {
    Categories.CHANNEL: "Channel",
    Categories.TUNNEL: "Tunnel",
    Categories.PORE: "Pore",
    Categories.SOLVENT_TUNNEL: "Solvent tunnel",
    Categories.SUBSTRATE_TUNNEL: "Substrate tunnel",
    Categories.SUBSTRATE_PRODUCT_TUNNEL: "Substrate/Product tunnel",
    Categories.PRODUCT_TUNNEL: "Product tunnel",
    Categories.WATER_CHANNEL: "Water channel",
    Categories.ION_CHANNEL: "Ion channel",
    Categories.HYDROPHOBIC_CHANNEL: "Hydrophobic channel",
    Categories.PEPTIDE_CHANNEL: "Peptide channel",
    Categories.NUCLEOTIDE_CHANNEL: "Nucleotide channel",
}

CATEGORIES_NAME_TO_ID = {
    "Channel": Categories.CHANNEL.value,
    "Tunnel": Categories.TUNNEL.value,
    "Pore": Categories.PORE.value,
    "Solvent tunnel": Categories.SOLVENT_TUNNEL.value,
    "Substrate tunnel": Categories.SUBSTRATE_TUNNEL.value,
    "Substrate/Product tunnel": Categories.SUBSTRATE_PRODUCT_TUNNEL.value,
    "Product tunnel": Categories.PRODUCT_TUNNEL.value,
    "Water channel": Categories.WATER_CHANNEL.value,
    "Ion channel": Categories.ION_CHANNEL.value,
    "Hydrophobic channel": Categories.HYDROPHOBIC_CHANNEL.value,
    "Peptide channel": Categories.PEPTIDE_CHANNEL.value,
    "Nucleotide channel": Categories.NUCLEOTIDE_CHANNEL.value,
}


class CategoryBase(SQLModel):
    name: str = Field(index=True)


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="category")
