"""Database models for channel profiles.

This module defines SQLModel classes for storing and retrieving channel profile data,
which represents the geometric properties of channels at different points
along their length.
"""

from decimal import Decimal
from typing import TYPE_CHECKING, Annotated

from pydantic import PlainSerializer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.database.models import Channel


class ProfileBase(SQLModel):
    """Base model for channel profile data.

    Attributes:
        radius: Radius of the channel at this point.
        free_radius: Free radius of the channel at this point.
        t_value: Parameter value along the channel path.
        coord_x: X coordinate of the point.
        coord_y: Y coordinate of the point.
        coord_z: Z coordinate of the point.
        distance: Distance along the channel path.
        charge: Net charge at this point.
    """

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
    """Model for inserting new channel profiles.

    Attributes:
        channel_id: Foreign key reference to the associated channel.
    """

    channel_id: int = Field(foreign_key="channel.id")


class Profile(ProfileInsert, table=True):
    """Database model for channel profiles.

    Attributes:
        id: Primary key for the profile.
        channel: Associated channel.
    """

    id: int = Field(primary_key=True)

    channel: "Channel" = Relationship(back_populates="profiles")


class ProfileOutput(ProfileBase):
    """Model for channel profile data in API responses."""

    pass
