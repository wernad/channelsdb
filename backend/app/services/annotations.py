from sqlmodel import Session

from app.database.models import AnnotationOutput, AnnotationInsert
from app.database.repositories import AnnotationRepository


class AnnotationService:
    repository: AnnotationRepository

    def __init__(self, db: Session):
        self.repository = AnnotationRepository(db)

    def get_annotations_by_structure(self, internal_id: str) -> list[AnnotationOutput]:
        """Fetches annotations for given structure and returns it as a dict."""

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
        """Inserts values into annotation table in bulk."""
        result = self.repository.insert_in_bulk(values=values)

        if result:
            return result
        return None

    def insert_entry(self, values: AnnotationInsert) -> int:
        """Inserts a single row into annotation table."""

        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
