from sqlmodel import func, insert, select, and_

from app.database.models import (
    Channel,
    ChannelInsert,
    Category,
    Method,
    ChannelFilter,
    Structure,
    Profile,
    Residue,
    Layer,
)
from app.database.repositories.base import RepositoryBase
from app.log import log


class ChannelRepository(RepositoryBase):
    """Repository for DB operations related to ."""

    def _build_filter_statement(self, filter: ChannelFilter) -> str:
        """Build query using passed filter argument.

        Args:
            filter: dataclass with variables to filter by.

        Returns:
            query object.
        """
        log.debug(f"Building filter statement with params: {filter}")

        statement = select(Structure.id).join(
            Channel, Channel.structure_id == Structure.id
        )

        # Profile related conditions.
        profile_conditions = []

        if filter.min_radius is not None:
            profile_conditions.append(Profile.radius >= filter.min_radius)
        if filter.max_radius is not None:
            profile_conditions.append(Profile.radius <= filter.max_radius)

        if filter.min_distance is not None:
            profile_conditions.append(Profile.distance >= filter.min_distance)
        if filter.max_distance is not None:
            profile_conditions.append(Profile.distance <= filter.max_distance)

        # Layer related conditions.
        bottleneck_condition = None

        if filter.min_bottleneck is not None:
            bottleneck_condition = and_(
                Layer.bottleneck, Layer.radius >= filter.min_bottleneck
            )

        # Apply conditions, if any.
        if profile_conditions:
            statement = statement.join(Profile, Profile.channel_id == Channel.id)

            for cond in profile_conditions:
                statement.filter(cond)

        if bottleneck_condition:
            statement = statement.join(Layer, Layer.channel_id == Channel.id)

        # Offset and limit.
        statement = statement.offset(filter.offset).limit(filter.limit)

        # Remove duplicates.
        statement = statement.distinct()

        log.debug("Statement build successfully.")
        return statement

    def get_channels_filtered(self, filter: ChannelFilter):
        statement = self._build_filter_statement(filter)
        channels = self.db.exec(statement).all()
        return channels

    def get_channels_by_structure_id(self, structure_id: int) -> list[Channel]:
        statement = select(Channel).where(Channel.structure_id == structure_id)
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

    def get_channel_counts_by_id(self, structure_id: int) -> list[tuple]:
        statement = (
            select(
                Method.name.label("method"),
                func.count(Channel.id).label("count"),
            )
            .join(Channel, Channel.method_id == Method.id)
            .group_by(Method.name)
            .where(Channel.structure_id == structure_id)
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

        if result:
            counts = {name: count for name, count in result}

            return counts

        return None

    def get_top_channel_counts_per_category_ratio(self, limit: int = 5) -> dict:
        """Returns top N categories based on channel counts as ratios.

        Args:
            limit: limits number of entries.
        Returns:
            result as dictionary with names as keys and counts as values.
        """

        statement = (
            select(Category.name, func.count(Channel.id).label("count"))
            .join(Channel, Channel.category_id == Category.id)
            .group_by(Category.name)
            .order_by(func.count(Channel.id).desc())
            .limit(limit)
        )

        category_result = self.db.exec(statement).mappings().all()
        statement = select(func.count(Channel.id))
        total_result = self.db.exec(statement).first()

        if category_result:
            counts = {entry["name"]: entry["count"] for entry in category_result}
            counts["total"] = total_result

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
