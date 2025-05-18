from sqlmodel import Session

from app.database.models import StructureData, StructureInsert, Structure, ChannelFilter
from app.database.repositories import StructureRepository


class StructureService:
    repository: StructureRepository

    def __init__(self, db: Session):
        self.repository = StructureRepository(db)

    def check_if_exists_by_external_id_and_version(
        self, external_id: str, version: int
    ) -> Structure | None:
        """Checks if given structure exists with external id and version."""
        result = self.repository.get_structure_by_external_id_and_version(
            external_id, version
        )

        if result:
            return result

        return None

    def update_has_channels_by_internal_id(
        self, internal_id: int, has_channels: bool
    ) -> None:
        """Updates has_channels column of given protein entry."""

        result = self.repository.update_has_channels_by_internal_id(
            internal_id, has_channels
        )

        if result:
            return result

        return None

    def get_structures_by_filter(self, filter: ChannelFilter) -> list[str]:
        result = self.repository.get_structures_by_channel_filter(filter)

        return result

    def get_source_and_version_by_external_id(self, external_id: str) -> StructureData:
        result = self.repository.get_source_and_version_by_external_id(
            external_id=external_id
        )

        return StructureData(**result)

    def get_newest_structure_with_channels_by_external_id(
        self, external_id: str
    ) -> int:
        structure = self.repository.get_newest_structure_has_channels_by_external_id(
            external_id=external_id
        )

        if structure:
            return structure.id

        return None

    def insert_entry(self, values: StructureInsert) -> int:
        """Inserts a single row into layer table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None

    def get_external_from_internal_bulk(self, internal_ids: list[int]) -> list[str]:
        """Returns list of external ids from corresponding internal ids."""

        result = self.repository.get_external_from_internal_bulk(internal_ids)

        if result:
            return result

        return None

    def get_latest_version_by_external_id(self, external_id: str) -> int:
        result = self.repository.get_latest_version_by_external_id(
            external_id=external_id
        )

        return result

    def delete_structure_by_external_id(self, external_id: str) -> None:
        internal_id = self.repository.delete_structure(external_id)

        return internal_id
