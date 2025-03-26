from datetime import date

from fastapi import APIRouter
from sqlmodel import SQLModel

from app.api.dependencies import StatisticsServiceDep


router = APIRouter()


class StatisticsModel(SQLModel):
    date: date
    entries_count: int
    statistics: dict[str, int]


@router.get(
    "/statistics",
    name="General statistics",
    description="Returns summary statistics about the data stored",
    response_model=StatisticsModel,
)
async def get_channel_counts_by_software_method(
    statistics_service: StatisticsServiceDep,
):
    statistics = statistics_service.get_channel_counts_by_software_method()

    if statistics:
        result = StatisticsModel(**statistics)
        return result

    return {}
