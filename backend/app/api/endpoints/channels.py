from fastapi import HTTPException, APIRouter

from app.database.models.channel import Channels
from channelsdb.backend.app.api.dependencies import ChannelsRepositoryDep
from app.api.common import (
    SourceDatabase,
    PDB_ID_Type,
    Uniprot_ID_Type,
    pdb_id_404_response,
    uniprot_id_404_response,
)

router = APIRouter()


@router.get(
    "/channels/pdb/{pdb_id}",
    response_model=Channels,
    name="Channel data",
    tags=["PDB"],
    description="Returns information about channels for a given protein",
    responses=pdb_id_404_response,
)
async def get_channels_pdb(pdb_id: PDB_ID_Type):
    return get_channels(SourceDatabase.PDB, pdb_id)


@router.get(
    "/channels/alphafill/{uniprot_id}",
    response_model=Channels,
    name="Channel data",
    tags=["AlphaFill"],
    description="Returns information about channels for a given protein",
    responses=uniprot_id_404_response,
)
async def get_channels_alphafill(uniprot_id: Uniprot_ID_Type):
    return get_channels(SourceDatabase.AlphaFill, uniprot_id)


# TODO add DB facade.
def get_channels(
    source_db: SourceDatabase, protein_id: str, channel_repo: ChannelsRepositoryDep
):
    channels = channel_repo.find_channels_by_structure_id(structure_id=protein_id)

    if not channels:
        raise HTTPException(
            status_code=404,
            detail=f"Protein with ID '{protein_id}' not asdasdasdasdsafound in ChannelsDB ({source_db.value})",
        )

    return channels


# @router.get(
#     path="/channels/filter",
#     response_model=list[Channels],
#     name="Filtered channels",
#     tags=["PDB", "Alphafil"],
#     description="Returns list of channels based on passed filter.",
# )
# async def get_channels_filter(filter: ChannelsFilter): ...
