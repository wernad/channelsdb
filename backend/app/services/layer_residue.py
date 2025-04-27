from sqlmodel import Session

from app.database.models import LayerResidueInsert
from app.database.repositories import LayerResidueRepository


class LayerResidueService:
    repository: LayerResidueRepository

    def __init__(self, db: Session):
        self.repository = LayerResidueRepository(db)

    def insert_bulk(self, values: list[LayerResidueInsert]) -> list[int]:
        """Inserts values into layer residue table in bulk."""
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: LayerResidueInsert) -> int:
        """Inserts a single row into layer residue table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
