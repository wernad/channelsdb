from sqlmodel import insert, select

from app.database.models import CATEGORIES_ID_TO_NAME, Categories, Category
from app.database.repositories.base import RepositoryBase
from app.log import log


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
            {"id": category.value, "name": CATEGORIES_ID_TO_NAME[category]}
            for category in Categories
        ]
        statement = insert(Category).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined categories: {values}")
        return True
