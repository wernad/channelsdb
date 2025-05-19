"""Repository module for managing channel data.

This module provides the ChannelRepository class for database operations related to
channels, including retrieving channel counts, filtering by structure ID, and inserting
new channels in bulk or individually.
"""

from sqlmodel import func, insert, select

from app.database.models import (
    Channel,
    ChannelInsert,
    Method,
    Structure,
)
from app.database.repositories.base import RepositoryBase
from app.log import log


class ChannelRepository(RepositoryBase):
    """Repository for managing channel data.

    This class provides methods for retrieving channel statistics, filtering channels
    by various criteria, and inserting new channels. It supports operations like
    counting channels per method, finding top channels by protein, and bulk insertions.
    """

    def get_total_channels(self) -> int:
        """Returns the total number of channels in the database.

        Returns:
            Total count of channels.
        """
        statement = select(func.count(Channel.id))
        total = self.db.exec(statement).first()

        return total

    def get_channels_by_internal_id(self, internal_id: int) -> list[Channel]:
        """Retrieves all channels for a given structure.

        Args:
            internal_id: The internal ID of the structure.

        Returns:
            List of Channel objects associated with the structure.
        """
        statement = select(Channel).where(Channel.structure_id == internal_id)
        channels = self.db.exec(statement).all()

        return channels

    def get_channel_counts_per_method(self) -> list[tuple]:
        """Retrieves the count of channels for each detection method.

        Returns:
            List of tuples containing method names and their channel counts,
            ordered by count in descending order.
        """
        statement = (
            select(
                Method.name.label("method"),
                func.count(Channel.id).label("count"),
            )
            .join(Channel, Channel.method_id == Method.id)
            .group_by(Method.name)
            .order_by(func.count(Channel.id).desc())
        )

        counts = self.db.exec(statement).all()

        return counts

    def get_channel_counts_per_methods_by_internal_id(
        self, internal_id: int
    ) -> list[tuple]:
        """Retrieves channel counts per method for a specific structure.

        Args:
            internal_id: The internal ID of the structure.

        Returns:
            List of tuples containing method names and their channel counts for the structure,
            ordered by count in descending order.
        """
        statement = (
            select(
                Method.name.label("method"),
                func.count(Channel.id).label("count"),
            )
            .join(Channel, Channel.method_id == Method.id)
            .group_by(Method.name)
            .where(Channel.structure_id == internal_id)
            .order_by(func.count(Channel.id).desc())
        )

        counts = self.db.exec(statement).all()
        return counts

    def get_top_5_channel_counts_per_protein(self, limit: int = 5) -> dict:
        """Returns top N channel counts per protein.

        Args:
            limit: Maximum number of entries to return.

        Returns:
            Dictionary with protein external IDs as keys and channel counts as values,
            including a 'total' key with the overall channel count.
        """
        statement = (
            select(Structure.external_id, func.count(Channel.id).label("count"))
            .join(Channel, Channel.structure_id == Structure.id)
            .group_by(Structure.external_id)
            .order_by(func.count(Channel.id).desc())
            .limit(limit)
        )

        result = self.db.exec(statement).all()
        total = self.get_total_channels()
        if result:
            counts = {name: count for name, count in result}
            counts["total"] = total
            return counts

        return {}

    def get_top_n_channel_counts_per_type(self, limit: int = 5) -> dict:
        """Returns ratio of top N channel types by channel counts.

        Args:
            limit: Maximum number of channel types to return.

        Returns:
            Dictionary with channel types as keys and counts as values,
            including a 'total' key with the overall channel count.
        """
        statement = (
            select(Channel.type, func.count(Channel.id).label("count"))
            .group_by(Channel.type)
            .order_by(func.count(Channel.id).desc())
            .limit(limit)
        )

        result = self.db.exec(statement).mappings().all()
        total = self.get_total_channels()

        if result:
            counts = {entry["type"]: entry["count"] for entry in result}
            counts["total"] = total

            return counts
        return None

    def insert_in_bulk(self, values: list[ChannelInsert]) -> list[int]:
        """Inserts multiple channel records in a single database operation.

        Args:
            values: List of ChannelInsert objects to insert.

        Returns:
            List of IDs for the newly inserted channels.
        """
        values = [value.model_dump() for value in values]
        statement = insert(Channel).values(values).returning(Channel.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: ChannelInsert) -> int:
        """Inserts a single channel record.

        Args:
            values: ChannelInsert object containing the channel data.

        Returns:
            ID of the newly inserted channel.
        """
        statement = insert(Channel).values(values.model_dump()).returning(Channel.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
