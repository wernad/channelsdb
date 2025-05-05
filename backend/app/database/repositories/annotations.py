from sqlmodel import select, insert

from app.database.models import Annotation, AnnotationInsert, Channel
from app.database.repositories.base import RepositoryBase


class AnnotationRepository(RepositoryBase):
    def get_annotations_by_structure_id(self, internal_id: str) -> list[Annotation]:
        statement = (
            select(Annotation)
            .join(Channel, Channel.id == Annotation.channel_id)
            .where(Channel.structure_id == internal_id)
        )
        annotations = self.db.exec(statement).all()

        return annotations

    def insert_in_bulk(self, values: list[AnnotationInsert]) -> list[int]:
        """Inserts new annotation rows in bulk."""
        values = [value.model_dump() for value in values]
        statement = insert(Annotation).values(values).returning(Annotation.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: AnnotationInsert) -> int:
        """Inserts a new channel entry."""

        statement = (
            insert(Annotation).values(values.model_dump()).returning(Annotation.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
