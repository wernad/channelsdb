from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import (
    AnnotationServiceDep,
    ChannelServiceDep,
    IDCheckDep,
    StructureServiceDep,
)
from app.api.exceptions import NoChannelsInProtein, ProteinNotFound, NoChannelWithFilter
from app.database.models import ChannelsResponse, ChannelFilter

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
        channels = channels_service.get_channels_with_by_structure(
            structure_id=internal_id,
        )
        if not channels:
            raise ProteinNotFound(protein_id=structure_id)
    else:
        raise NoChannelsInProtein(protein_id=structure_id)

    annotations = ann_service.get_annotations_by_structure(internal_id=internal_id)

    return ChannelsResponse(annotations=annotations, channels=channels)


@router.get(
    path="/filter/",
    response_model=list[str],
    name="Filtered proteins",
    description="Returns list of protein ids based on passed filter.",
)
async def get_channels_filtered(
    structure_service: StructureServiceDep,
    channels_service: ChannelServiceDep,
    filter: Annotated[ChannelFilter, Query()],
):

    internal_ids = channels_service.get_channels_by_filter(filter)

    if internal_ids:
        external_ids = structure_service.get_external_from_internal_bulk(internal_ids)

        return external_ids

    raise NoChannelWithFilter()
