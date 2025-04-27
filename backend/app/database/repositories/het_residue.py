from sqlmodel import insert

from app.database.models import HetResidue, HetResidueInsert
from app.database.repositories.base import RepositoryBase


class HetResidueRepository(RepositoryBase):
    """Repository for DB operations related to het residues."""

    def insert_in_bulk(self, values: list[HetResidueInsert]) -> list[int]:
        """Inserts new het residue rows in bulk."""

        values = [value.model_dump() for value in values]
        statement = insert(HetResidue).values(values).returning(HetResidue.id)

        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: HetResidueInsert) -> int:
        """Inserts a new het residue entry."""

        statement = (
            insert(HetResidue).values(**values.model_dump()).returning(HetResidue.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
