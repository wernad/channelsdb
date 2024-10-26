from sqlmodel import Field, SQLModel
from decimal import Decimal


class ProfileBase(SQLModel):
    radius: Decimal = Field(decimal_places=3)
    free_radius: Decimal = Field(decimal_places=3)
    t_value: Decimal = Field(decimal_places=3)
    coord_x: Decimal = Field(decimal_places=3)
    coord_y: Decimal = Field(decimal_places=3)
    coord_z: Decimal = Field(decimal_places=3)
    distance: Decimal = Field(decimal_places=3)
    charge: int


class Profile(ProfileBase, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")


class ProfileOutput(ProfileBase):
    pass
