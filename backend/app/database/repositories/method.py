from sqlmodel import insert, select
from app.database.repositories.base import RepositoryBase
from app.database.models import Method, Methods, METHODS_NAMES

from app.log import logger as log


class MethodRepository(RepositoryBase):

    def init_table(self):
        statement = select(Method.id, Method.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Methods table is not empty, skipping initialization. Present methods: {result}"
            )
            return False

        values = [
            {"id": method.value, "name": METHODS_NAMES[method]} for method in Methods
        ]
        statement = insert(Method).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined methods: {values}")

        return True
