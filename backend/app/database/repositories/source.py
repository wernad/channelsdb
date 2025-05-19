"""Repository module for managing protein structure sources."""

from sqlmodel import insert, select

from app.database.models import Source, Sources
from app.database.repositories.base import RepositoryBase
from app.log import log

# Mapping of source enums to their display names
SOURCES_NAMES = {Sources.PDB: "pdb", Sources.ALPHAFILL: "alphafill"}


class SourceRepository(RepositoryBase):
    """Repository for managing protein structure sources.

    This class provides methods for initializing the sources table with predefined
    structure sources and their mappings.
    """

    def init_table(self):
        """Initializes the sources table with predefined structure sources.

        Checks if the sources table is empty and, if so, populates it with
        predefined sources from the Sources enum.

        Returns:
            bool: True if the table was initialized, False if it was already populated.
        """
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
