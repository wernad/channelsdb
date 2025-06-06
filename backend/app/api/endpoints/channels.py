"""Endpoints for retrieving channel data for proteins."""

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
    """Returns channels and annotations of them for given protein id.

    Args:
        structure_service: Service object for retrieving structure data from database.
        channels_service: Service object for retrieving channel data from database.
        ann_service: Service object for retrieving annotation data from database.
        structure_id: Id of structure in PDB or UniProt format.
    """
    internal_id = structure_service.get_newest_structure_with_channels_by_external_id(
        external_id=structure_id
    )

    if internal_id:
        channels = channels_service.get_channels_with_by_structure_internal_id(
            internal_id=internal_id,
        )
        if not channels:
            raise ProteinNotFound(protein_id=structure_id)
    else:
        raise NoChannelsInProtein(protein_id=structure_id)

    annotations = ann_service.get_annotations_by_structure_internal_id(
        internal_id=internal_id
    )

    return ChannelsResponse(annotations=annotations, channels=channels)
