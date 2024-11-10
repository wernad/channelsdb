from sqlmodel import select
from app.database.repositories.base import RepositoryBase
from app.database.models.annotation import Annotation


class AnnotationRepository(RepositoryBase):
    def get_annotations_by_structure_id(self, structure_id: str) -> list[Annotation]:
        statement = select(Annotation).where(Annotation.structure_id == structure_id)
        annotations = self.db.exec(statement).all()

        return annotations
