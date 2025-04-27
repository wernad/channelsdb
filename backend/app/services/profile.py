from sqlmodel import Session

from app.database.models import ProfileInsert
from app.database.repositories import ProfileRepository


class ProfileService:
    repository: ProfileRepository

    def __init__(self, db: Session):
        self.repository = ProfileRepository(db)

    def insert_bulk(self, values: list[ProfileInsert]) -> list[int]:
        """Inserts values into profile table in bulk."""
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: ProfileInsert) -> int:
        """Inserts a single row into profile table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
