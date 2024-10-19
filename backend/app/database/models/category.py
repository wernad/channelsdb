from sqlmodel import Field, SQLModel, Relationship
from app.database.models import Channel


class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    channels: list[Channel] = Relationship(back_populates="category")
