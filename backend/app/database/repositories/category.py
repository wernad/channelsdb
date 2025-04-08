from sqlmodel import insert, select
from app.database.repositories.base import RepositoryBase
from app.database.models import Category, Categories

from app.log import logger as log


CATEGORIES_NAMES = {Categories.Tunnel: "Tunnel"}


class CategoryRepository(RepositoryBase):

    def init_table(self):
        statement = select(Category.id, Category.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Categories table is not empty, skipping initialization. Present categories: {result}"
            )
            return False

        values = [
            {"id": category.value, "name": CATEGORIES_NAMES[category]}
            for category in Categories
        ]
        statement = insert(Category).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined categories: {values}")
        return True
