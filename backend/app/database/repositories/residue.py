from sqlmodel import insert, select, func, distinct

from app.database.models import RESIDUES_VALUES, Residue, Residues, LayerResidue, Layer
from app.database.repositories.base import RepositoryBase
from app.log import log


class ResidueRepository(RepositoryBase):

    def init_table(self):
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
        """Returns top 5 residues by number of channels it is in.

        Args:
            limit: limits number of entries.
        Returns:
            result as dictionary with residue names as keys and counts as values.
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
        print(statement)
        result = self.db.exec(statement).all()

        if result:
            counts = {name: count for name, count in result}

            return counts
        return {}
