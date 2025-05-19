"""Repository module for managing channel detection methods.

This module provides the MethodRepository class for database operations related to
channel detection methods, including initializing the methods table with predefined
detection algorithms and their mappings.
"""

from sqlmodel import insert, select

from app.database.models import METHODS_IDS_TO_NAMES, Method, Methods
from app.database.repositories.base import RepositoryBase
from app.log import log


class MethodRepository(RepositoryBase):
    """Repository for managing channel detection methods.

    This class provides methods for initializing and managing the methods table,
    which stores predefined channel detection algorithms names.
    """

    def init_table(self):
        """Initializes the methods table with predefined detection methods.

        Checks if the methods table is empty and, if so, populates it with
        predefined channel detection methods from the Methods enum.

        Returns:
            bool: True if the table was initialized, False if it was already populated.
        """
        statement = select(Method.id, Method.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Methods table is not empty, skipping initialization. Present methods: {result}"
            )
            return False

        values = [
            {"id": method.value, "name": METHODS_IDS_TO_NAMES[method]}
            for method in Methods
        ]
        statement = insert(Method).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined methods: {values}")

        return True
