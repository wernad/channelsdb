from enum import Enum
from typing import TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel


class Methods(Enum):
    CSA_TUNNELS_MOLE = 1
    CSA_TUNNELS_CAVER = 2
    REVIEWED_CHANNELS_MOLE = 3
    REVIEWED_CHANNELS_CAVER = 4
    COFACTOR_TUNNELS_MOLE = 5
    COFACTOR_TUNNELS_CAVER = 6
    TRANSMEMBRANE_PORES_MOLE = 7
    TRANSMEMBRANE_PORES_CAVER = 8
    PROCOGNATE_TUNNELS_MOLE = 9
    PROCOGNATE_TUNNELS_CAVER = 10
    ALPHAFILL_TUNNELS_MOLE = 11
    ALPHAFILL_TUNNELS_CAVER = 12


class MethodBase(SQLModel):
    name: str = Field(index=True)


class Method(MethodBase, table=True):
    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="method")
