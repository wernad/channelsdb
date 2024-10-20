from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from app.database.models import Channel


class MethodBase(SQLModel):
    name: str = Field(index=True)


class Method(MethodBase, table=True):
    id: int = Field(primary_key=True)

    channels: list["Channel"] = Relationship(back_populates="method")
