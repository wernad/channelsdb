"""Database models for channel detection methods.

This module defines SQLModel classes for storing and retrieving channel detection methods,
including enumerations for different method types and their mappings to database records.
"""

from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class Methods(Enum):
    """Enumeration of available channel detection methods.

    Each method represents a specific combination of detection algorithm (MOLE/Caver)
    and channel type (CSA tunnels, reviewed channels, etc.).
    """

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


# Mapping of method IDs to their display names
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

# Mapping of method display names to their IDs
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
    """Base model for channel detection methods.

    Attributes:
        name: Name of the detection method.
    """

    name: str = Field(index=True)


class Method(MethodBase, table=True):
    """Database model for channel detection methods.

    Attributes:
        id: Primary key for the method.
        channels: List of channels detected using this method.
    """

    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="method")
