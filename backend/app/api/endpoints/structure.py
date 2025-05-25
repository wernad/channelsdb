"""Endpoints for filtering structures based on their parameters
and parameters of related tables (channel, layer, etc).
"""

from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import StructureServiceDep
from app.api.exceptions import NoStructuresWithFilter, NoStructuresWithActiveChannels
from app.database.models import ChannelFilter, StructurePagination

router = APIRouter()


@router.get(
    path="/filter",
    response_model=list[str],
    name="Filtered proteins",
    description="Returns list of protein ids based on passed filter.",
)
async def get_structures_filtered(
    structure_service: StructureServiceDep,
    filter: Annotated[ChannelFilter, Query()],
):
    """Returns protein ids based on parameters of their channels.

    Args:
        structure_service: Service object to retrieve structure data.
        filter: Parameter to filter by.
    Returns:
        List of strings.
    """
    external_ids = structure_service.get_structures_by_filter(filter)

    if external_ids:

        return external_ids

    raise NoStructuresWithFilter()


@router.get(
    path="/all",
    response_model=list[str],
    name="All active structures",
    description="Returns all curently stored entries that contain channels.",
)
async def get_all_structures(
    structure_service: StructureServiceDep,
    pagination: Annotated[StructurePagination, Query()],
):
    """Returns list of external ids of proteins stored database with channels.

    Uses pagination.

    Args:
        structure_service: Service object to retrieve structure data.
        pagination: Limit and offset.
    Returns:
        List of strings.
    """

    result = structure_service.get_all_active_structures_with_pagination(
        pagination.limit, pagination.offset
    )

    if not result:
        raise NoStructuresWithActiveChannels()

    return result
