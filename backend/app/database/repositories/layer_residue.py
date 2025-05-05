from sqlmodel import insert
from app.database.models import LayerResidue, LayerResidueInsert
from app.database.repositories.base import RepositoryBase


class LayerResidueRepository(RepositoryBase):
    """Repository for DB operations related to residues in layers."""

    def insert_in_bulk(self, values: list[LayerResidueInsert]) -> list[int]:
        """Inserts new residues in a specific layer in bulk."""

        values = [value.model_dump() for value in values]

        statement = insert(LayerResidue).values(values).returning(LayerResidue.id)

        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: LayerResidueInsert) -> int:
        """Inserts a new residue in layer entry."""

        statement = (
            insert(LayerResidue).values(values.model_dump()).returning(LayerResidue.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
