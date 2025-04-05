from typing import TYPE_CHECKING, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Structure


class SourceBase(SQLModel):
    name: str = Field(index=True)


class Source(SourceBase, table=True):
    id: int = Field(primary_key=True)

    structures: List["Structure"] = Relationship(back_populates="source")
