from sqlmodel import Session
from app.database.repositories import StructureRepository

from app.database.models import StructureData


class StructureService:
    repository: StructureRepository

    def __init__(self, db: Session):
        self.repository = StructureRepository(db)

    def get_source_and_version_by_id(self, external_id: str) -> StructureData:
        result = self.repository.get_structure_by_external_id(external_id=external_id)

        return StructureData.model_validate(result)

    def get_internal_id_if_has_channels(self, structure_id: str) -> int:
        structure = self.repository.get_structure_with_channels_by_external_id(
            structure_id=structure_id
        )

        if structure:
            return structure.id
