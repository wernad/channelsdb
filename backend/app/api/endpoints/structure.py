"""Endpoints for filtering structures based on their parameters
and parameters of related tables (channel, layer, etc).
"""

from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import StructureServiceDep
from app.api.exceptions import NoStructuresWithFilter
from app.database.models import ChannelFilter

router = APIRouter()


@router.get(
    path="/filter/",
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
