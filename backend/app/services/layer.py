"""Service module for managing channel layers.

This module provides the LayerService class for handling business logic related to
channel layers, including bulk and individual insertions of layer data.
"""

from sqlmodel import Session

from app.database.models import LayerInsert
from app.database.repositories import LayerRepository


class LayerService:
    """Service for managing channel layers.

    This class provides methods for inserting layer data into the database,
    handling both bulk and individual insertions. It acts as a business logic
    layer between the API and the database repository.
    """

    repository: LayerRepository

    def __init__(self, db: Session):
        """Initialize the LayerService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = LayerRepository(db)

    def insert_bulk(self, values: list[LayerInsert]) -> list[int]:
        """Inserts multiple layer records in a single operation.

        Args:
            values: List of LayerInsert objects containing layer data to insert.

        Returns:
            List of IDs for the newly inserted layers, or None if insertion failed.
        """
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: LayerInsert) -> int:
        """Inserts a single layer record.

        Args:
            values: LayerInsert object containing the layer data to insert.

        Returns:
            ID of the newly inserted layer, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
