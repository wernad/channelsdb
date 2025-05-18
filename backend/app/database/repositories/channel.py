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
    """Repository for DB operations related to ."""

    def get_total_channels(self) -> int:
        """Returns total number of channels."""
        statement = select(func.count(Channel.id))
        total = self.db.exec(statement).first()

        return total

    def get_channels_by_internal_id(self, internal_id: int) -> list[Channel]:
        statement = select(Channel).where(Channel.structure_id == internal_id)
        channels = self.db.exec(statement).all()

        return channels

    def get_channel_counts_per_method(self) -> list[tuple]:
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
            limit: limits number of entries.
        Returns:
            result as dictionary with protein external ids as keys and counts as values.
        """

        statement = (
            select(Structure.external_id, func.count(Channel.id).label("count"))
            .join(Channel, Channel.structure_id == Structure.id)
            .group_by(Structure.external_id)
            .order_by(func.count(Channel.id).desc())
            .limit(limit)
        )

        result = self.db.exec(statement).all()
        total = total = self.get_total_channels()
        if result:
            counts = {name: count for name, count in result}
            counts["total"] = total
            return counts

        return {}

    def get_top_n_channel_counts_per_type(self, limit: int = 5) -> dict:
        """Returns ratio of top N channel types by channel counts.

        Args:
            limit: limits number of entries.
        Returns:
            result as dictionary with names as keys and counts as values.
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
        """Inserts new channel rows in bulk."""
        values = [value.model_dump() for value in values]
        statement = insert(Channel).values(values).returning(Channel.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: ChannelInsert) -> int:
        """Inserts a new channel entry."""

        statement = insert(Channel).values(values.model_dump()).returning(Channel.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
