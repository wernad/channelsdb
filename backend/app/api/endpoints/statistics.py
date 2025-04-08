from datetime import date

from fastapi import APIRouter
from sqlmodel import SQLModel

from app.api.dependencies import StatisticsServiceDep, StructureServiceDep

from app.api.exceptions import NoChannelsInProtein

router = APIRouter()


class StatisticsModel(SQLModel):
    date: date
    entries_count: int
    statistics: dict[str, int]


@router.get(
    "/",
    name="General statistics",
    description="Returns summary statistics about the data stored",
    response_model=StatisticsModel,
)
async def get_channel_counts_per_category(
    statistics_service: StatisticsServiceDep,
):
    statistics = statistics_service.get_channel_counts_per_category()

    if statistics:
        result = StatisticsModel(**statistics)
        return result

    return {}


@router.get(
    "/{structure_id}",
    name="General statistics",
    description="Returns summary statistics about the data stored",
    response_model=StatisticsModel,
)
async def get_channel_counts_by_id(
    structure_id: str,
    structure_service: StructureServiceDep,
    statistics_service: StatisticsServiceDep,
):
    internal_id = structure_service.get_internal_id_if_has_channels(structure_id)

    if internal_id:
        statistics = statistics_service.get_channel_counts_by_id(internal_id)

        if statistics:
            result = StatisticsModel(**statistics)
            return result

    raise NoChannelsInProtein(protein_id=structure_id)
