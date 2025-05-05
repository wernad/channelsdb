from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

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


METHODS_IDS_TO_NAMES = {
    Methods.CSA_TUNNELS_MOLE: "CSATunnels_MOLE",
    Methods.CSA_TUNNELS_CAVER: "CSATunnels_Caver",
    Methods.REVIEWED_CHANNELS_MOLE: "ReviewedChannels_MOLE",
    Methods.REVIEWED_CHANNELS_CAVER: "ReviewedChannels_Caver",
    Methods.COFACTOR_TUNNELS_MOLE: "CofactorTunnels_MOLE",
    Methods.COFACTOR_TUNNELS_CAVER: "CofactorTunnels_Caver",
    Methods.TRANSMEMBRANE_PORES_MOLE: "TransmembranePores_MOLE",
    Methods.TRANSMEMBRANE_PORES_CAVER: "TransmembranePores_Caver",
    Methods.PROCOGNATE_TUNNELS_MOLE: "ProcognateTunnels_MOLE",
    Methods.PROCOGNATE_TUNNELS_CAVER: "ProcognateTunnels_Caver",
    Methods.ALPHAFILL_TUNNELS_MOLE: "AlphaFillTunnels_MOLE",
    Methods.ALPHAFILL_TUNNELS_CAVER: "AlphaFillTunnels_Caver",
}

METHODS_NAMES_TO_IDS = {
    "CSATunnels_MOLE": Methods.CSA_TUNNELS_MOLE,
    "CSATunnels_Caver": Methods.CSA_TUNNELS_CAVER,
    "ReviewedChannels_MOLE": Methods.REVIEWED_CHANNELS_MOLE,
    "ReviewedChannels_Caver": Methods.REVIEWED_CHANNELS_CAVER,
    "CofactorTunnels_MOLE": Methods.COFACTOR_TUNNELS_MOLE,
    "CofactorTunnels_Caver": Methods.COFACTOR_TUNNELS_CAVER,
    "TransmembranePores_MOLE": Methods.TRANSMEMBRANE_PORES_MOLE,
    "TransmembranePores_Caver": Methods.TRANSMEMBRANE_PORES_CAVER,
    "ProcognateTunnels_MOLE": Methods.PROCOGNATE_TUNNELS_MOLE,
    "ProcognateTunnels_Caver": Methods.PROCOGNATE_TUNNELS_CAVER,
    "AlphaFillTunnels_MOLE": Methods.ALPHAFILL_TUNNELS_MOLE,
    "AlphaFillTunnels_Caver": Methods.ALPHAFILL_TUNNELS_CAVER,
}


class MethodBase(SQLModel):
    name: str = Field(index=True)


class Method(MethodBase, table=True):
    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="method")
