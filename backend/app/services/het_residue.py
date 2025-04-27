from sqlmodel import Session

from app.database.models import HetResidueInsert
from app.database.repositories import HetResidueRepository


class HetResidueService:
    repository: HetResidueRepository

    def __init__(self, db: Session):
        self.repository = HetResidueRepository(db)

    def insert_bulk(self, values: list[HetResidueInsert]) -> list[int]:
        """Inserts values into het residue table in bulk."""
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: HetResidueInsert) -> int:
        """Inserts a single row into het residue table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
