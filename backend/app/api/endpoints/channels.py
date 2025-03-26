from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel

from app.api.dependencies import ChannelServiceDep, AnnotationServiceDep, IDCheckDep
from app.api.exceptions import ProteinNotFound

from app.database.models import AnnotationOutput, ChannelOutput

router = APIRouter()


class ChannelsResponse(BaseModel):
    annotations: List[AnnotationOutput] = []
    channels: Dict[str, List[ChannelOutput]]


@router.get(
    "/{protein_id}",
    response_model=ChannelsResponse,
    name="Channel data",
    description="Returns information about channels for a given protein",
)
async def get_channels(
    channels_service: ChannelServiceDep,
    ann_service: AnnotationServiceDep,
    protein_id: IDCheckDep,
):
    channels = channels_service.get_channels_with_annotations_by_structure(
        structure_id=protein_id,
    )
    if not channels:
        raise ProteinNotFound(protein_id=protein_id)

    annotations = ann_service.get_annotations_by_structure(structure_id=protein_id)
    return {"annotations": annotations, "channels": channels}


# @router.get(
#     path="/channels/filter",
#     response_model=list[Channels],
#     name="Filtered channels",
#     tags=["PDB", "Alphafil"],
#     description="Returns list of channels based on passed filter.",
# )
# async def get_channels_filter(filter: ChannelsFilter): ...
