from fastapi import APIRouter

from app.api.dependencies import (
    AnnotationServiceDep,
    ChannelServiceDep,
    IDCheckDep,
    StructureServiceDep,
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
    internal_id = structure_service.get_newest_structure_with_channels_by_external_id(
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
