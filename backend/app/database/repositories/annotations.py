"""Repository module for managing annotations in the database."""

from sqlmodel import select, insert

from app.database.models import Annotation, AnnotationInsert, Channel
from app.database.repositories.base import RepositoryBase


class AnnotationRepository(RepositoryBase):
    """Repository for managing annotations.

    This class provides methods for retrieving and inserting channel annotations,
    with support for bulk operations.
    """

    def get_annotations_by_internal_id(self, internal_id: str) -> list:
        """Retrieves all annotations for channels in a given structure.

        Args:
            internal_id: The internal ID of the structure.

        Returns:
            A list of annotations associated with the structure.
        """
        statement = (
            select(Annotation)
            .join(Channel, Channel.id == Annotation.channel_id)
            .where(Channel.structure_id == internal_id)
        )
        annotations = self.db.exec(statement).all()

        return annotations

    def insert_in_bulk(self, values: list[AnnotationInsert]) -> list[int]:
        """Inserts multiple annotation records in a single database operation.

        Args:
            values: List of AnnotationInsert objects to insert.

        Returns:
            List of IDs for the newly inserted annotations.
        """
        values = [value.model_dump() for value in values]
        statement = insert(Annotation).values(values).returning(Annotation.id)
        result = self.db.exec(statement)

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: AnnotationInsert) -> int:
        """Inserts a single annotation record.

        Args:
            values: AnnotationInsert object containing the annotation data.

        Returns:
            ID of the newly inserted annotation.
        """
        statement = (
            insert(Annotation).values(values.model_dump()).returning(Annotation.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
