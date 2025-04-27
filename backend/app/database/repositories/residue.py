from sqlmodel import insert, select

from app.database.models import RESIDUES_VALUES, Residue, Residues
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
