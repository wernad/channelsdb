"""Service module for managing residues in channel layers.

This module provides the LayerResidueService class for handling business logic related to
residues within channel layers, including bulk and individual insertions of layer residue data.
"""

from sqlmodel import Session

from app.database.models import LayerResidueInsert
from app.database.repositories import LayerResidueRepository


class LayerResidueService:
    """Service for managing residues in channel layers.

    This class provides methods for inserting layer residue data into the database,
    handling both bulk and individual insertions. It acts as a business logic
    layer between the API and the database repository.
    """

    repository: LayerResidueRepository

    def __init__(self, db: Session):
        """Initialize the LayerResidueService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = LayerResidueRepository(db)

    def insert_bulk(self, values: list[LayerResidueInsert]) -> list[int]:
        """Inserts multiple layer residue records in a single operation.

        Args:
            values: List of LayerResidueInsert objects containing layer residue data to insert.

        Returns:
            List of IDs for the newly inserted layer residues, or None if insertion failed.
        """
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: LayerResidueInsert) -> int:
        """Inserts a single layer residue record.

        Args:
            values: LayerResidueInsert object containing the layer residue data to insert.

        Returns:
            ID of the newly inserted layer residue, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
