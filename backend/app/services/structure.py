from sqlmodel import Session

from app.database.models import StructureData, StructureInsert
from app.database.repositories import StructureRepository


class StructureService:
    repository: StructureRepository

    def __init__(self, db: Session):
        self.repository = StructureRepository(db)

    def check_if_exists_by_external_id(self, external_id: str) -> int | None:
        """Checks if given structure exists using external id."""
        result = self.repository.get_structure_by_external_id(external_id)

        if result:
            return result.id
        return None

    def get_source_and_version_by_id(self, external_id: str) -> StructureData:
        result = self.repository.get_structure_by_external_id(external_id=external_id)

        return StructureData.model_validate(result)

    def get_internal_id_if_has_channels(self, structure_id: str) -> int:
        structure = self.repository.get_structure_with_channels_by_external_id(
            structure_id=structure_id
        )

        if structure:
            return structure.id

    def insert_entry(self, values: StructureInsert) -> int:
        """Inserts a single row into layer table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
