"""Repository module for managing channel profiles.

This module provides the ProfileRepository class for database operations related to
channel profiles, including inserting new profile data in bulk or individually.
"""

from sqlmodel import insert

from app.database.models import Profile, ProfileInsert
from app.database.repositories.base import RepositoryBase


class ProfileRepository(RepositoryBase):
    """Repository for managing channel profiles.

    This class provides methods for inserting channel profile data into the database,
    with support for both bulk and individual insertions.
    """

    def insert_in_bulk(self, values: list[ProfileInsert]) -> list[int]:
        """Inserts multiple profile records in a single database operation.

        Args:
            values: List of ProfileInsert objects to insert.

        Returns:
            List of IDs for the newly inserted profiles.
        """
        values = [value.model_dump() for value in values]
        statement = insert(Profile).values(values).returning(Profile.id)

        result = self.db.exec(statement)

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: ProfileInsert) -> int:
        """Inserts a single profile record.

        Args:
            values: ProfileInsert object containing the profile data.

        Returns:
            ID of the newly inserted profile.
        """
        statement = insert(Profile).values(values.model_dump()).returning(Profile.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
