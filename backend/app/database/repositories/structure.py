from sqlmodel import select
from app.database.repositories.base import RepositoryBase
from app.database.models import Structure


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
