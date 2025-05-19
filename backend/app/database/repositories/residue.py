"""Repository module for managing protein residues.

This module provides the ResidueRepository class for database operations related to
protein residues, including initializing the residues table with predefined amino acids
and retrieving residue statistics.
"""

from sqlmodel import insert, select, func, distinct

from app.database.models import RESIDUES_VALUES, Residue, Residues, LayerResidue, Layer
from app.database.repositories.base import RepositoryBase
from app.log import log


class ResidueRepository(RepositoryBase):
    """Repository for managing protein residues.

    This class provides methods for initializing the residues table with predefined
    amino acids and retrieving statistics about residue occurrences in channels.
    """

    def init_table(self):
        """Initializes the residues table with predefined amino acids.

        Checks if the residues table is empty and, if so, populates it with
        predefined amino acids from the Residues enum and their properties.

        Returns:
            bool: True if the table was initialized, False if it was already populated.
        """
        statement = select(Residue.id, Residue.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Residues table is not empty, skipping initialization. Present residues: {result}"
            )
            return False

        values = [
            {"id": residue.value, **RESIDUES_VALUES[residue]} for residue in Residues
        ]
        statement = insert(Residue).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined residues: {values}")
        return True

    def get_top_residue_counts_by_channels(self, limit: int = 5) -> dict:
        """Returns the most common residues in channels.

        Args:
            limit: Maximum number of residues to return.

        Returns:
            Dictionary with residue names as keys and their channel counts as values,
            ordered by count in descending order.
        """
        statement = (
            select(
                Residue.name,
                func.count(distinct(Layer.channel_id)).label("count"),
            )
            .join(LayerResidue, LayerResidue.residue_id == Residue.id)
            .join(Layer, Layer.id == LayerResidue.layer_id)
            .group_by(Residue.name)
            .order_by(func.count(distinct(Layer.channel_id)).desc())
            .limit(limit)
        )
        result = self.db.exec(statement).all()

        if result:
            counts = {name: count for name, count in result}

            return counts
        return {}
