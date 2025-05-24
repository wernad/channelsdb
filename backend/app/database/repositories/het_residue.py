"""Repository module for managing hetero residues.

This module provides the HetResidueRepository class for database operations related to
hetero residues, including inserting new residues in bulk or individually.
"""

from sqlmodel import insert

from app.database.models import HetResidue, HetResidueInsert
from app.database.repositories.base import RepositoryBase


class HetResidueRepository(RepositoryBase):
    """Repository for managing hetero residues.

    This class provides methods for inserting hetero residues into the database,
    with support for both bulk and individual insertions.
    """

    def insert_in_bulk(self, values: list[HetResidueInsert]) -> list[int]:
        """Inserts multiple hetero residue records in a single database operation.

        Args:
            values: List of HetResidueInsert objects to insert.

        Returns:
            List of IDs for the newly inserted hetero residues.
        """
        values = [value.model_dump() for value in values]
        statement = insert(HetResidue).values(values).returning(HetResidue.id)

        result = self.db.exec(statement)

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: HetResidueInsert) -> int:
        """Inserts a single het residue record.

        Args:
            values: HetResidueInsert object containing the hetero residue data.

        Returns:
            ID of the newly inserted hetero residue.
        """
        statement = (
            insert(HetResidue).values(**values.model_dump()).returning(HetResidue.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
