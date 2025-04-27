from decimal import Decimal
from typing import TYPE_CHECKING, Annotated

from pydantic import PlainSerializer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class ProfileBase(SQLModel):
    radius: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "Radius"})
    free_radius: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "FreeRadius"})
    t_value: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "T"})
    coord_x: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "X"})
    coord_y: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "Y"})
    coord_z: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "Z"})
    distance: Annotated[
        Decimal,
        PlainSerializer(lambda x: float(x), return_type=float, when_used="json"),
    ] = Field(decimal_places=3, schema_extra={"serialization_alias": "Distance"})
    charge: int = Field(schema_extra={"serialization_alias": "Charge"})


class ProfileInsert(ProfileBase):
    channel_id: int = Field(foreign_key="channel.id")


class Profile(ProfileInsert, table=True):
    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="profiles")


class ProfileOutput(ProfileBase):
    pass
