from sqlmodel import Session
from app.database.repositories.base import RepositoryBase


class ServiceBase:
    _repository_class: RepositoryBase

    def __init__(self, db: Session):
        self.repository = self._repository_class(db)
