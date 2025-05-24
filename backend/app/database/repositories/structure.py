"""Repository module for managing protein structures."""

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
    """Repository for managing protein structures.

    This class provides methods for retrieving, filtering, and managing protein structures,
    including version control, channel filtering, and bulk operations.
    """

    def get_structure_by_external_id_and_version(
        self, external_id: str, version: int
    ) -> tuple:
        """Retrieves a structure by its external ID and version.

        Args:
            external_id: External identifier of the structure (e.g., PDB ID).
            version: Version number of the structure.

        Returns:
            Row object matching the criteria.
        """
        statement = select(Structure).where(
            and_(Structure.external_id == external_id, Structure.version == version)
        )
        result = self.db.exec(statement).first()

        return result

    def get_newest_structure_has_channels_by_external_id(
        self, external_id: str
    ) -> tuple:
        """Retrieves the newest version of a structure that has channels.

        Args:
            external_id: External identifier of the structure.

        Returns:
            Tuple containing the structure ID and the highest version number that has channels.
        """
        statement = (
            select(Structure.id, func.max(Structure.version))
            .where(and_(Structure.external_id == external_id, Structure.has_channels))
            .group_by(Structure.id)
        )

        result = self.db.exec(statement).first()

        return result

    def get_source_and_version_by_external_id(self, external_id: str) -> dict:
        """Returns source and version information for a structure.

        Args:
            external_id: External identifier of the structure.

        Returns:
            Dictionary containing source_id and version of the structure.
        """
        version = self.get_latest_version_by_external_id(external_id)
        statement = select(Structure.source_id).where(
            Structure.external_id == external_id
        )

        result = self.db.exec(statement).first()

        return {"source_id": result, "version": version}

    def get_external_from_internal_bulk(self, internal_ids: list[int]) -> list[str]:
        """Converts internal IDs to external IDs.

        Args:
            internal_ids: List of internal structure IDs.

        Returns:
            List of corresponding external IDs.
        """
        statement = select(Structure.external_id).where(Structure.id.in_(internal_ids))

        result = self.db.exec(statement).all()

        return result

    def _build_filter_statement(self, filter: ChannelFilter) -> str:
        """Builds a query statement based on channel filter criteria.

        Args:
            filter: ChannelFilter object containing filtering criteria.

        Returns:
            SQL query statement for filtering structures by channel properties.
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
            func.max(Structure.version).label("version"),
        ).join(Channel, Channel.structure_id == Structure.id)

        if any(filter_ is not None for filter_ in filters):
            statement = statement.join(Profile, Profile.channel_id == Channel.id)

        if filter.min_bottleneck is not None:
            statement = statement.join(Layer, Layer.channel_id == Channel.id)
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

        statement = statement.order_by(Structure.external_id).group_by(
            Structure.external_id,
        )

        print("@", statement)

        log.debug("Statement build successfully.")
        return statement

    def get_structures_by_channel_filter(self, filter: ChannelFilter):
        """Retrieves structures based on channel filter criteria.

        Args:
            filter: ChannelFilter object containing filtering criteria.

        Returns:
            List of external IDs for structures matching the filter criteria.
        """
        statement = self._build_filter_statement(filter)
        result = self.db.exec(statement).all()

        external_ids = []
        if result:
            external_ids = [external_id for external_id, _ in result]

        return external_ids

    def update_has_channels_by_internal_id(
        self, internal_id: int, has_channels: bool
    ) -> None:
        """Updates the has_channels flag for a structure.

        Args:
            internal_id: Internal ID of the structure.
            has_channels: New value for the has_channels flag.
        """
        statement = select(Structure).where(Structure.id == internal_id)
        result = self.db.exec(statement).one()

        if result:
            result.has_channels = has_channels
            self.db.add(result)
            self.db.commit()

    def insert_in_bulk(self, values: list[StructureInsert]) -> list[int]:
        """Inserts multiple structure records in a single database operation.

        Args:
            values: List of StructureInsert objects to insert.

        Returns:
            List of IDs for the newly inserted structures.
        """
        values = [value.model_dump() for value in values]
        statement = insert(Structure).values(values).returning(Structure.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: StructureInsert) -> int:
        """Inserts a single structure record.

        Args:
            values: StructureInsert object containing the structure data.

        Returns:
            ID of the newly inserted structure.
        """
        statement = (
            insert(Structure).values(values.model_dump()).returning(Structure.id)
        )
        result = self.db.exec(statement)

        id = result.first()

        if id:
            id = id[0]

        return id

    def delete_structure(self, external_id: str) -> None:
        """Deletes a structure and its associated data.

        Args:
            external_id: External identifier of the structure to delete.
        """
        statement = select(Structure).where(Structure.external_id == external_id)
        structure = self.db.exec(statement).first()

        if structure:
            self.db.delete(structure)
            self.db.commit()
        else:
            log.error(f"Structure doesn't exist, can not delete: {external_id=}")

    def get_latest_version_by_external_id(self, external_id: str) -> int:
        """Retrieves the latest version number for a structure.

        Args:
            external_id: External identifier of the structure.

        Returns:
            Latest version number for the structure.
        """
        statement = select(func.max(Structure.version)).where(
            Structure.external_id == external_id
        )

        result = self.db.exec(statement).first()

        return result
