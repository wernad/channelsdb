from sqlmodel import insert

from app.database.models import Layer, LayerInsert
from app.database.repositories.base import RepositoryBase


class LayerRepository(RepositoryBase):
    """Repository for DB operations related to layers."""

    def insert_in_bulk(self, values: list[LayerInsert]) -> list[int]:
        """Inserts new layer rows in bulk."""

        values = [value.model_dump() for value in values]
        statement = insert(Layer).values(values).returning(Layer.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: LayerInsert) -> int:
        """Inserts a new layer entry."""

        statement = insert(Layer).values(values.model_dump()).returning(Layer.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
