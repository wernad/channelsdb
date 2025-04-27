from sqlmodel import insert

from app.database.models import Profile, ProfileInsert
from app.database.repositories.base import RepositoryBase


class ProfileRepository(RepositoryBase):
    """Repository for DB operations related to tunnel profile."""

    def insert_in_bulk(self, values: list[ProfileInsert]) -> list[int]:
        """Inserts new profile data of given tunnel in bulk."""
        values = [value.model_dump() for value in values]
        statement = insert(Profile).values(values).returning(Profile.id)

        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: ProfileInsert) -> int:
        """Inserts a new profile entry."""

        statement = insert(Profile).values(values.model_dump()).returning(Profile.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
