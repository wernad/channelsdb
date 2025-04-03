OLD_PDB_ID_REGEX = "^[1-9][a-z0-9]{3}$"
NEW_PDB_ID_REGEX = "^pdb_[0-9]{5}[a-z0-9]{3}$"
UNIPROT_ID_REGEX = (
    "[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$"
)


CHANNEL_TYPES_PDB = {
    "csa": "CSATunnels_MOLE",
    "cscaver": "CSATunnels_Caver",
    "authors": "ReviewedChannels_MOLE",
    "aucaver": "ReviewedChannels_Caver",
    "cofactors": "CofactorTunnels_MOLE",
    "cocaver": "CofactorTunnels_Caver",
    "pores": "TransmembranePores_MOLE",
    "pocaver": "TransmembranePores_Caver",
    "procognate": "ProcognateTunnels_MOLE",
    "procaver": "ProcognateTunnels_Caver",
}

CHANNEL_TYPES_ALPHAFILL = {
    "alphafill": "AlphaFillTunnels_MOLE",
    "alphacaver": "AlphaFillTunnels_Caver",
}

CHANNEL_TYPES = CHANNEL_TYPES_PDB | CHANNEL_TYPES_ALPHAFILL
