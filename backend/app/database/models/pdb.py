from sqlmodel import SQLModel, Field


class PDBDataBase(SQLModel):
    has_channels: bool


class PDBData(PDBDataBase, table=True):
    structure_id: str = Field(primary_key=True)
