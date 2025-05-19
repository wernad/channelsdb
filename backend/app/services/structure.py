"""Service module for managing protein structures.

This module provides the StructureService class for handling business logic related to
protein structures, including version control, channel filtering, and structure management.
"""

from sqlmodel import Session

from app.database.models import StructureData, StructureInsert, Structure, ChannelFilter
from app.database.repositories import StructureRepository


class StructureService:
    """Service for managing protein structures.

    This class provides methods for managing protein structures, including version control,
    channel filtering, and structure management operations. It acts as a business logic
    layer between the API and the database repository.
    """

    repository: StructureRepository

    def __init__(self, db: Session):
        """Initialize the StructureService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = StructureRepository(db)

    def check_if_exists_by_external_id_and_version(
        self, external_id: str, version: int
    ) -> Structure | None:
        """Checks if a structure exists with the given external ID and version.

        Args:
            external_id: External identifier of the structure (e.g., PDB ID).
            version: Version number of the structure.

        Returns:
            Structure object if found, None otherwise.
        """
        result = self.repository.get_structure_by_external_id_and_version(
            external_id, version
        )

        if result:
            return result

        return None

    def update_has_channels_by_internal_id(
        self, internal_id: int, has_channels: bool
    ) -> None:
        """Updates the has_channels flag for a structure.

        Args:
            internal_id: Internal ID of the structure.
            has_channels: New value for the has_channels flag.
        """
        _ = self.repository.update_has_channels_by_internal_id(
            internal_id, has_channels
        )

        return None

    def get_structures_by_filter(self, filter: ChannelFilter) -> list[str]:
        """Retrieves structures based on channel filter criteria.

        Args:
            filter: ChannelFilter object containing filtering criteria.

        Returns:
            List of external IDs for structures matching the filter criteria.
        """
        result = self.repository.get_structures_by_channel_filter(filter)

        return result

    def get_source_and_version_by_external_id(self, external_id: str) -> StructureData:
        """Retrieves source and version information for a structure.

        Args:
            external_id: External identifier of the structure.

        Returns:
            StructureData object containing source_id and version information.
        """
        result = self.repository.get_source_and_version_by_external_id(
            external_id=external_id
        )

        return StructureData(**result)

    def get_newest_structure_with_channels_by_external_id(
        self, external_id: str
    ) -> int:
        """Retrieves the newest version of a structure that has channels.

        Args:
            external_id: External identifier of the structure.

        Returns:
            Internal ID of the newest structure with channels, or None if not found.
        """
        structure = self.repository.get_newest_structure_has_channels_by_external_id(
            external_id=external_id
        )

        if structure:
            return structure.id

        return None

    def insert_entry(self, values: StructureInsert) -> int:
        """Inserts a single structure record.

        Args:
            values: StructureInsert object containing the structure data.

        Returns:
            ID of the newly inserted structure, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None

    def get_external_from_internal_bulk(self, internal_ids: list[int]) -> list[str]:
        """Converts internal IDs to external IDs.

        Args:
            internal_ids: List of internal structure IDs.

        Returns:
            List of corresponding external IDs, or None if conversion failed.
        """
        result = self.repository.get_external_from_internal_bulk(internal_ids)

        if result:
            return result

        return None

    def get_latest_version_by_external_id(self, external_id: str) -> int:
        """Retrieves the latest version number for a structure.

        Args:
            external_id: External identifier of the structure.

        Returns:
            Latest version number for the structure.
        """
        result = self.repository.get_latest_version_by_external_id(
            external_id=external_id
        )

        return result

    def delete_structure_by_external_id(self, external_id: str) -> None:
        """Deletes a structure and its associated data.

        Args:
            external_id: External identifier of the structure to delete.
        """
        internal_id = self.repository.delete_structure(external_id)

        return internal_id
