"""Service module for managing channel profiles.

This module provides the ProfileService class for handling business logic related to
channel profiles, including bulk and individual insertions of profile data.
"""

from sqlmodel import Session

from app.database.models import ProfileInsert
from app.database.repositories import ProfileRepository


class ProfileService:
    """Service for managing channel profiles.

    This class provides methods for inserting channel profile data into the database,
    handling both bulk and individual insertions. It acts as a business logic
    layer between the API and the database repository.
    """

    repository: ProfileRepository

    def __init__(self, db: Session):
        """Initialize the ProfileService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = ProfileRepository(db)

    def insert_bulk(self, values: list[ProfileInsert]) -> list[int]:
        """Inserts multiple profile records in a single operation.

        Args:
            values: List of ProfileInsert objects containing profile data to insert.

        Returns:
            List of IDs for the newly inserted profiles, or None if insertion failed.
        """
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: ProfileInsert) -> int:
        """Inserts a single profile record.

        Args:
            values: ProfileInsert object containing the profile data to insert.

        Returns:
            ID of the newly inserted profile, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
