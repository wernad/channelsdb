from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel

from app.api.dependencies import ChannelServiceDep, AnnotationServiceDep
from app.api.exceptions import ProteinNotFound
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
async def get_channels(channels_service: ChannelServiceDep, ann_service: AnnotationServiceDep, structure_id: str):
    print("@@@@@@", "panda")
    channels = channels_service.get_channels_by_structure_json(
        structure_id=structure_id,
    )

    annotations = ann_service.get_annotations_by_structure_json(structure_id=structure_id)

    if not channels:
        raise ProteinNotFound(protein_id=structure_id)
    return {"annotations": annotations, "channels": channels}


# @router.get(
#     path="/channels/filter",
#     response_model=list[Channels],
#     name="Filtered channels",
#     tags=["PDB", "Alphafil"],
#     description="Returns list of channels based on passed filter.",
# )
# async def get_channels_filter(filter: ChannelsFilter): ...
