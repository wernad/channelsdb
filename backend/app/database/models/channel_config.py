from sqlmodel import Field, SQLModel, JSON


# TODO not used yet
class ConfigFile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    config_file: dict = Field(sa_type=JSON)
