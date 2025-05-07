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

    external_ids = structure_service.get_structures_by_filter(filter)

    if external_ids:

        return external_ids

    raise NoStructuresWithFilter()
