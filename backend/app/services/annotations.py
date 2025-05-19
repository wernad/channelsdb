"""Service module for managing channel annotations.

This module provides the AnnotationService class for handling business logic related to
channel annotations, including retrieving annotations for structures and inserting
new annotations in bulk or individually.
"""

from sqlmodel import Session

from app.database.models import AnnotationOutput, AnnotationInsert
from app.database.repositories import AnnotationRepository


class AnnotationService:
    """Service for managing channel annotations.

    This class provides methods for retrieving and inserting channel annotations,
    handling both bulk and individual operations. It acts as a business logic
    layer between the API and the database repository.
    """

    repository: AnnotationRepository

    def __init__(self, db: Session):
        """Initialize the AnnotationService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = AnnotationRepository(db)

    def get_annotations_by_structure(self, internal_id: str) -> list[AnnotationOutput]:
        """Retrieves all annotations for channels in a given structure.

        Args:
            internal_id: Internal ID of the structure.

        Returns:
            List of AnnotationOutput objects containing channel annotations.
        """
        annotations = self.repository.get_annotations_by_structure_id(internal_id)

        result = []

        for ann in annotations:
            result.append(
                AnnotationOutput(
                    id=ann.channel_id,
                    name=ann.name,
                    description=ann.description,
                    reference=ann.reference,
                    reference_type=ann.reference_type,
                )
            )

        return result

    def insert_bulk(self, values: list[AnnotationInsert]) -> list[int]:
        """Inserts multiple annotation records in a single operation.

        Args:
            values: List of AnnotationInsert objects containing annotation data to insert.

        Returns:
            List of IDs for the newly inserted annotations, or None if insertion failed.
        """
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: AnnotationInsert) -> int:
        """Inserts a single annotation record.

        Args:
            values: AnnotationInsert object containing the annotation data to insert.

        Returns:
            ID of the newly inserted annotation, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
