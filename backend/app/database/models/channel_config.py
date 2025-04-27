from sqlmodel import JSON, Field, Relationship, SQLModel

from app.database.models import Channel

# # TODO not used yet
# class ConfigFile(SQLModel, table=True):
#     id: int = Field(primary_key=True)
#     channel_id: int = Field(foreign_key="channel.id")
#     config_file: dict = Field(sa_type=JSON)

#     channel: Channel = Relationship(back_populates="config_file")
