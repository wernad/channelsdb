from sqlmodel import Session

from app.database.models import LayerInsert
from app.database.repositories import LayerRepository


class LayerService:
    repository: LayerRepository

    def __init__(self, db: Session):
        self.repository = LayerRepository(db)

    def insert_bulk(self, values: list[LayerInsert]) -> list[int]:
        """Inserts values into layer table in bulk."""
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: LayerInsert) -> int:
        """Inserts a single row into layer table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
