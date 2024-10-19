from sqlmodel import Field, SQLModel, Relationship
from app.database.models import Channel


class Method(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    channels: list[Channel] = Relationship(back_populates="method")
