"""Repository module for managing residues in channel layers.

This module provides the LayerResidueRepository class for database operations related to
residues within channel layers, including inserting new layer residues in bulk or individually.
"""

from sqlmodel import insert
from app.database.models import LayerResidue, LayerResidueInsert
from app.database.repositories.base import RepositoryBase


class LayerResidueRepository(RepositoryBase):
    """Repository for managing residues in channel layers.

    This class provides methods for inserting residues into channel layers,
    with support for both bulk and individual insertions.
    """

    def insert_in_bulk(self, values: list[LayerResidueInsert]) -> list[int]:
        """Inserts multiple layer residue records in a single database operation.

        Args:
            values: List of LayerResidueInsert objects to insert.

        Returns:
            List of IDs for the newly inserted layer residues.
        """
        values = [value.model_dump() for value in values]

        statement = insert(LayerResidue).values(values).returning(LayerResidue.id)

        result = self.db.exec(statement)

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: LayerResidueInsert) -> int:
        """Inserts a single layer residue record.

        Args:
            values: LayerResidueInsert object containing the layer residue data.

        Returns:
            ID of the newly inserted layer residue.
        """
        statement = (
            insert(LayerResidue).values(values.model_dump()).returning(LayerResidue.id)
        )
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
