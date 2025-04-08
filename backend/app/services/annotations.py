from sqlmodel import Session
from app.database.repositories import AnnotationRepository
from app.database.models import AnnotationOutput


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
