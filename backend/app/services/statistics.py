"""Service module for managing channel statistics.

This module provides the StatisticsService class for handling business logic related to
channel statistics, including method counts, protein counts, residue frequencies,
and geometric measurements of channels.
"""

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
    """Service for managing channel statistics.

    This class provides methods for retrieving and aggregating various statistics about
    channels, including counts by method, protein, and residue type, as well as
    geometric measurements like channel lengths and bottleneck radii.
    """

    channel_repository: ChannelRepository
    layer_repository: LayerRepository
    residue_repository: ResidueRepository

    def __init__(self, db: Session):
        """Initialize the StatisticsService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.channel_repository = ChannelRepository(db)
        self.layer_repository = LayerRepository(db)
        self.residue_repository = ResidueRepository(db)

    def get_channel_counts_per_method(self) -> dict:
        """Retrieves channel counts for each detection method.

        Returns:
            Dictionary containing:
            - date: Current date
            - entries_count: Total number of channels
            - statistics: Dictionary mapping method names to their channel counts
        """
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
        """Retrieves channel counts per method for a specific structure.

        Args:
            internal_id: Internal ID of the structure.

        Returns:
            Dictionary containing:
            - date: Current date
            - entries_count: Total number of channels in the structure
            - statistics: Dictionary mapping method names to their channel counts
        """
        result = self.channel_repository.get_channel_counts_per_methods_by_internal_id(
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
        """Retrieves the top 5 proteins with the most channels.

        Returns:
            Dictionary mapping protein external IDs to their channel counts,
            including a 'total' key with the overall channel count.
        """
        result = self.channel_repository.get_top_5_channel_counts_per_protein()

        if not result:
            return None

        total = self.channel_repository.get_total_channels()

        result["total"] = total

        return result

    def get_top_5_residues_by_channel_count(self) -> list[str]:
        """Retrieves the top 5 most common residues in channels.

        Residues are counted based on the residues in the channel residues, not the layers.

        Returns:
            Dictionary mapping residue names to their channel counts,
            including a 'total' key with the overall channel count.
        """
        result = self.residue_repository.get_top_residue_counts_by_channels()

        if not result:
            return None

        total = self.channel_repository.get_total_channels()
        result["total"] = total

        return result

    def get_top_5_types_by_channel_count(self) -> dict:
        """Retrieves the top 5 channel types by count.

        Returns:
            Dictionary mapping channel types to their counts,
            including a 'total' key with the overall channel count.
        """
        result = self.channel_repository.get_top_n_channel_counts_per_type()

        if not result:
            return None

        return result

    def get_channel_length_stats(self) -> dict:
        """Retrieves statistical measures of channel lengths.

        Returns:
            Dictionary containing:
            - avg: Mean channel length
            - min: Minimum channel length
            - max: Maximum channel length
            - median: Median channel length
            - stdev: Standard deviation of channel lengths
            - min_structure: Structure that contains shortest channel.
            - max_structure: Structure that contains longest channel.
        """
        result = self.layer_repository.get_length_statistics()

        result = {
            key: (
                round(value, 3)
                if value is not None and not isinstance(value, str)
                else value
            )
            for key, value in result.items()
        }

        return result

    def get_channel_bottleneck_stats(self) -> dict:
        """Retrieves statistical measures of channel bottleneck radii.

        Returns:
            Dictionary containing:
            - avg: Mean bottleneck radius
            - min: Minimum bottleneck radius
            - max: Maximum bottleneck radius
            - median: Median bottleneck radius
            - stdev: Standard deviation of bottleneck radii
        """
        result = self.layer_repository.get_bottleneck_radius_statistics()
        result = {
            key: (round(value, 3) if value is not None else value)
            for key, value in result.items()
        }
        return result
