from datetime import date

from fastapi import APIRouter
from sqlmodel import SQLModel

from app.api.dependencies import IDCheckDep, StatisticsServiceDep, StructureServiceDep
from app.api.exceptions import NoChannelsInProtein, NoStatistics

router = APIRouter()


class StatisticsRaw(SQLModel):
    statistics: dict[str, int | float | None]


class StatisticsModel(StatisticsRaw):
    date: date
    entries_count: int


@router.get(
    "/methods",
    name="General statistics",
    description="Returns summary statistics about the data stored",
    response_model=StatisticsModel,
)
async def get_channel_counts_per_method(
    statistics_service: StatisticsServiceDep,
):
    statistics = statistics_service.get_channel_counts_per_method()

    if statistics:
        result = StatisticsModel(**statistics)
        return result

    return {}


@router.get(
    "/methods/{structure_id}",
    name="Overall channel counts per method.",
    description="Returns channel counts for each calculation method.",
    response_model=StatisticsModel,
)
async def get_channel_counts_per_methods_by_id(
    structure_id: IDCheckDep,
    structure_service: StructureServiceDep,
    statistics_service: StatisticsServiceDep,
):
    internal_id = structure_service.get_newest_structure_with_channels_by_external_id(
        external_id=structure_id
    )

    if internal_id:
        statistics = statistics_service.get_channel_counts_per_methods_by_id(
            internal_id
        )

        if statistics:
            result = StatisticsModel(**statistics)
            return result

    raise NoChannelsInProtein(protein_id=structure_id)


@router.get(
    "/length",
    name="General statistics about channel lengths",
    description="Returns statistics about lengths of channels.",
    response_model=StatisticsRaw,
)
async def get_length_stats(
    statistics_service: StatisticsServiceDep,
):

    statistics = statistics_service.get_channel_length_stats()

    if all(value is not None for value in statistics.values()):
        result = StatisticsRaw(statistics=statistics)
        return result
    raise NoStatistics()


@router.get(
    "/bottleneck",
    name="General statistics about bottlenecks",
    description="Returns statistics about lengths of channels.",
    response_model=StatisticsRaw,
)
async def get_bottleneck_stats(
    statistics_service: StatisticsServiceDep,
):

    statistics = statistics_service.get_channel_bottleneck_stats()

    if any(value is not None for value in statistics.values()):
        result = StatisticsRaw(statistics=statistics)
        return result
    raise NoStatistics()


@router.get(
    "/top_types",
    name="Top 5 types",
    description="Returns top 5 channel counts per channel type.",
    response_model=StatisticsRaw,
)
async def get_top_categories(
    statistics_service: StatisticsServiceDep,
):

    statistics = statistics_service.get_top_5_types_by_channel_count()

    if statistics:
        result = StatisticsRaw(statistics=statistics)
        return result
    raise NoStatistics()


@router.get(
    "/top_proteins",
    name="Top 5 proteins by channel count",
    description="Returns top proteins by their total channel count.",
    response_model=StatisticsRaw,
)
async def get_top_proteins(
    statistics_service: StatisticsServiceDep,
):

    statistics = statistics_service.get_top_5_proteins_by_channel_count()

    if statistics:
        result = StatisticsRaw(statistics=statistics)
        return result
    raise NoStatistics()


@router.get(
    "/top_residues",
    name="Top 5 residues by presence in channels.",
    description="Returns top residues by their presence in channels (not layer).",
    response_model=StatisticsRaw,
)
async def get_top_residues(
    statistics_service: StatisticsServiceDep,
):

    statistics = statistics_service.get_top_5_residues_by_channel_count()

    if statistics:
        result = StatisticsRaw(statistics=statistics)
        return result
    raise NoStatistics()
