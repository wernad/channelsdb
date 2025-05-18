from datetime import datetime as dt

from sqlmodel import Session

from app.database.models import METHODS_IDS_TO_NAMES
from app.database.repositories import (
    ChannelRepository,
    LayerRepository,
    ResidueRepository,
)
from app.log import log


class StatisticsService:
    channel_repository: ChannelRepository
    layer_repository: LayerRepository
    residue_repository: ResidueRepository

    def __init__(self, db: Session):
        self.channel_repository = ChannelRepository(db)
        self.layer_repository = LayerRepository(db)
        self.residue_repository = ResidueRepository(db)

    def get_channel_counts_per_method(self) -> dict:
        result = self.channel_repository.get_channel_counts_per_method()

        date = dt.now().date()
        if result:
            entries_count = sum(row.count for row in result)

            entries = {method: 0 for method in METHODS_IDS_TO_NAMES.values()}
            for row in result:
                entries[row.method] = row.count

            result = {
                "date": date,
                "entries_count": entries_count,
                "statistics": entries,
            }
        else:
            result = {
                "date": date,
                "entries_count": 0,
                "statistics": {},
            }

        return result

    def get_channel_counts_per_methods_by_id(self, internal_id: int) -> dict:
        result = self.channel_repository.get_channel_counts_per_methods_by_id(
            internal_id=internal_id
        )

        log.debug("Building statistics result.")
        date = dt.now().date()
        if result:
            entries_count = sum(row.count for row in result)

            entries = {method: 0 for method in METHODS_IDS_TO_NAMES.values()}
            for row in result:
                entries[row.method] = row.count

            result = {
                "date": date,
                "entries_count": entries_count,
                "statistics": entries,
            }
        else:
            result = {
                "date": date,
                "entries_count": 0,
                "statistics": {},
            }

        return result

    def get_top_5_proteins_by_channel_count(self) -> list[str]:
        """Returns top 5 external protein ids with most channels."""
        result = self.channel_repository.get_top_5_channel_counts_per_protein()

        if not result:
            return None

        total = self.channel_repository.get_total_channels()

        result["total"] = total

        return result

    def get_top_5_residues_by_channel_count(self) -> list[str]:
        "Returns top 5 most common residues in channels."
        result = self.residue_repository.get_top_residue_counts_by_channels()

        if not result:
            return None

        total = self.channel_repository.get_total_channels()
        result["total"] = total

        return result

    def get_top_5_types_by_channel_count(self) -> dict:
        """Returns top 5 types of channels."""
        result = self.channel_repository.get_top_n_channel_counts_per_type()

        if not result:
            return None

        return result

    def get_channel_length_stats(self) -> dict:
        """Returns mean, median, range and standard deviation of channels' lengths."""
        result = self.layer_repository.get_length_statistics()

        result = {
            key: (round(value, 3) if value is not None else value)
            for key, value in result.items()
        }

        return result

    def get_channel_bottleneck_stats(self) -> dict:
        """Returns mean, median, range and standard deviation of channels' radii."""
        result = self.layer_repository.get_bottleneck_radius_statistics()
        result = {
            key: (round(value, 3) if value is not None else value)
            for key, value in result.items()
        }
        return result
