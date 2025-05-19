"""Base repository module providing common functionality for all repositories."""

from sqlmodel import Session


class RepositoryBase:
    """Base class for all repository classes.

    Attributes:
        db: SQLModel database session instance.
    """

    def __init__(self, db: Session):
        self.db = db
