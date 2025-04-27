from sqlmodel import insert, select

from app.database.models import Structure, StructureInsert
from app.database.repositories.base import RepositoryBase


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
