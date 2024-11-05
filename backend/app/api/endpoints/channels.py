from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel

# from app.database.models.channel import Channels
from app.api.dependencies import ChannelServiceDep
from app.api.exceptions import ProteinNotFound, UnsupportedDBType
from app.api.common import (
    pdb_id_404_response,
)

router = APIRouter()


class Channels(BaseModel):
    annotations: List = []
    channels: Dict[str, list]


@router.get(
    "/{protein_id}",
    response_model=Channels,
    name="Channel data",
    tags=["PDB"],
    description="Returns information about channels for a given protein",
    responses=pdb_id_404_response,
)
async def get_channels(service: ChannelServiceDep, protein_id: str, db_type: str):
    if db_type not in ["pdb", "alphafil"]:
        raise UnsupportedDBType(db_type=db_type)

    channels = service.get_channels_by_structure_json(
        structure_id=protein_id,
    )

    if not channels:
        raise ProteinNotFound(protein_id=protein_id)
    return channels


# @router.get(
#     path="/channels/filter",
#     response_model=list[Channels],
#     name="Filtered channels",
#     tags=["PDB", "Alphafil"],
#     description="Returns list of channels based on passed filter.",
# )
# async def get_channels_filter(filter: ChannelsFilter): ...
