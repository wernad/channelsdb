from sqlmodel import insert, select, func, and_

from app.database.models import (
    Structure,
    Channel,
    StructureInsert,
    Profile,
    Layer,
    ChannelFilter,
)
from app.database.repositories.base import RepositoryBase


from app.log import log


class StructureRepository(RepositoryBase):
    def get_structure_by_external_id(self, external_id: str) -> tuple:
        statement = select(Structure).where(Structure.external_id == external_id)
        result = self.db.exec(statement).first()

        return result

    def get_structure_with_channels_by_external_id(
        self, structure_id: str
    ) -> Structure:
        statement = select(Structure).where(
            Structure.external_id == structure_id and Structure.has_channels
        )
        result = self.db.exec(statement).first()

        return result

    def get_external_from_internal_bulk(self, internal_ids: list[int]) -> list[str]:
        """Return a list of external ids from internal ids."""

        statement = select(Structure.external_id).where(Structure.id.in_(internal_ids))

        result = self.db.exec(statement).all()

        return result

    def _build_filter_statement(self, filter: ChannelFilter) -> str:
        """Build query using passed filter argument.

        Args:
            filter: dataclass with variables to filter by.

        Returns:
            query object.
        """
        log.debug(f"Building filter statement with params: {filter}")

        # Layer related conditions.
        conditions = []
        filters = [
            filter.min_radius,
            filter.max_radius,
            filter.min_distance,
            filter.max_distance,
        ]

        statement = select(
            Structure.external_id,
            func.max(Layer.end_distance).label("length"),
        ).join(Channel, Channel.structure_id == Structure.id)

        if any(filter_ is not None for filter_ in filters):
            statement = statement.join(Profile, Profile.channel_id == Channel.id)

        if filter.min_bottleneck is not None:
            statement = statement.join(Layer, Layer.channel_id == Channel.id).group_by(
                Structure.external_id
            )
            conditions.extend([Layer.bottleneck, Layer.radius >= filter.min_bottleneck])

        if filter.min_radius is not None:
            conditions.append(Profile.radius >= filter.min_radius)
        if filter.max_radius is not None:
            conditions.append(Profile.radius <= filter.max_radius)

        if filter.min_distance is not None:
            conditions.append(Profile.distance >= filter.min_distance)
        if filter.max_distance is not None:
            conditions.append(Profile.distance <= filter.max_distance)

        # Apply conditions, if any.
        if conditions:
            statement = statement.filter(and_(*conditions))

        # Offset and limit.
        statement = statement.offset(filter.offset).limit(filter.limit)

        statement = statement.group_by(
            Structure.external_id,
        )

        print("@", statement)

        log.debug("Statement build successfully.")
        return statement

    def get_structures_by_channel_filter(self, filter: ChannelFilter):
        statement = self._build_filter_statement(filter)
        result = self.db.exec(statement).all()

        external_ids = []
        if result:
            external_ids = [external_id for external_id, _ in result]

        return external_ids

    def update_has_channels_by_internal_id(
        self, internal_id: int, has_channels: bool
    ) -> None:
        """Updates has_channels column of protein with given internal id."""

        statement = select(Structure).where(Structure.id == internal_id)
        result = self.db.exec(statement).one()

        if result:
            result.has_channels = has_channels
            self.db.add(result)
            self.db.commit()

    def insert_in_bulk(self, values: list[StructureInsert]) -> list[int]:
        """Inserts new structure rows in bulk."""

        values = [value.model_dump() for value in values]
        statement = insert(Structure).values(values).returning(Structure.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: StructureInsert) -> int:
        """Inserts a new structure entry."""

        statement = (
            insert(Structure).values(values.model_dump()).returning(Structure.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()

        if id:
            id = id[0]

        return id
