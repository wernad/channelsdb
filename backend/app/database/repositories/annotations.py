from sqlmodel import select
from app.database.repositories.base import RepositoryBase
from app.database.models import Annotation


class AnnotationRepository(RepositoryBase):
    def get_annotations_by_structure_id(self, internal_id: str) -> list[Annotation]:
        statement = select(Annotation).where(Annotation.structure_id == internal_id)
        annotations = self.db.exec(statement).all()

        return annotations
