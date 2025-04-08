from typing import List, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Field

from app.api.dependencies import (
    ChannelServiceDep,
    AnnotationServiceDep,
    StructureServiceDep,
    IDCheckDep,
)
from app.api.exceptions import NoChannelsInProtein, ProteinNotFound

from app.database.models import ChannelsResponse

router = APIRouter()


@router.get(
    "/{structure_id}",
    response_model=ChannelsResponse,
    response_model_by_alias=True,
    name="Channel data",
    description="Returns information about channels for a given protein",
)
async def get_channels(
    structure_service: StructureServiceDep,
    channels_service: ChannelServiceDep,
    ann_service: AnnotationServiceDep,
    structure_id: IDCheckDep,
):
    internal_id = structure_service.get_internal_id_if_has_channels(
        structure_id=structure_id
    )

    if internal_id:
        channels = channels_service.get_channels_with_annotations_by_structure(
            structure_id=internal_id,
        )
        if not channels:
            raise ProteinNotFound(protein_id=structure_id)
    else:
        raise NoChannelsInProtein(protein_id=structure_id)

    annotations = ann_service.get_annotations_by_structure(internal_id=internal_id)

    return ChannelsResponse(annotations=annotations, channels=channels)


# @router.get(
#     path="/channels/filter",
#     response_model=list[Channels],
#     name="Filtered channels",
#     tags=["PDB", "Alphafil"],
#     description="Returns list of channels based on passed filter.",
# )
# async def get_channels_filter(filter: ChannelsFilter): ...
