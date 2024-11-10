from sqlmodel import Session
from app.database.repositories.annotations import AnnotationRepository


class AnnotationService:
    repository: AnnotationRepository

    def __init__(self, db: Session):
        self.repository = AnnotationRepository(db)

    def get_annotations_by_structure_json(self, structure_id: str):
        """Fetches annotations for given structure and returns it as a dict."""

        annotations = self.repository.get_annotations_by_structure_id(structure_id)

        result = []

        for ann in annotations:
            result.append(
                {
                    "Id": ann.channel_id,
                    "Name": ann.name,
                    "Description": ann.description,
                    "Reference": ann.reference,
                    "ReferenceType": ann.reference_type,
                }
            )

        return result
