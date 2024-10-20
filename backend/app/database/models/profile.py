from sqlmodel import Field, SQLModel


class ProfileBase(SQLModel):
    radius: float
    free_radius: float
    t_value: float
    coord_x: float
    coord_y: float
    coord_z: float
    distance: float
    charge: float


class Profile(ProfileBase, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")


class ProfileOutput(ProfileBase):
    pass
