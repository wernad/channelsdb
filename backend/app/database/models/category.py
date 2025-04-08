from enum import Enum
from typing import TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel


class Categories(Enum):
    Tunnel = 1


class CategoryBase(SQLModel):
    name: str = Field(index=True)


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)

    channels: List["Channel"] = Relationship(back_populates="category")
