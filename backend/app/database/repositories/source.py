from sqlmodel import insert, select
from app.database.repositories.base import RepositoryBase
from app.database.models import Source, Sources

from app.log import logger as log


SOURCES_NAMES = {Sources.PDB: "pdb", Sources.Alphafill: "alphafill"}


class SourceRepository(RepositoryBase):

    def init_table(self):
        statement = select(Source.id, Source.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Sources table is not empty, skipping initialization. Present sources: {result}"
            )
            return False

        values = [
            {"id": source.value, "name": SOURCES_NAMES[source]} for source in Sources
        ]
        statement = insert(Source).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined sources: {values}")
        return True
