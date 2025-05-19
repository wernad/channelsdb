"""Service module for managing het residues in channels."""

from sqlmodel import Session

from app.database.models import HetResidueInsert
from app.database.repositories import HetResidueRepository


class HetResidueService:
    """Service for managing het residues in channels.

    This service provides methods for inserting het residue data into the database,
    handling both bulk and individual insertions. It acts as a business logic layer
    between the API and the database repository.

    Attributes:
        repository (HetResidueRepository): Repository for accessing het residue data.
    """

    repository: HetResidueRepository

    def __init__(self, db: Session):
        """Initialize the het residue service with a database session.

        Args:
            db: SQLModel database session for accessing het residue data.
        """
        self.repository = HetResidueRepository(db)

    def insert_bulk(self, values: list[HetResidueInsert]) -> list[int]:
        """Insert multiple het residue records in a single operation.

        Args:
            values: List of het residue records to insert.

        Returns:
            List of IDs for the newly inserted het residues, or None if
                insertion failed.
        """
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: HetResidueInsert) -> int:
        """Insert a single het residue record.

        Args:
            values: het residue record to insert.

        Returns:
            ID of the newly inserted het residue, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
