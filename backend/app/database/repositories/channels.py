from sqlmodel import Session, select, join

from app.database.repositories.base import RepositoryBase
from app.database.models import Channel
from channelsdb.backend.app.database.structures import Filter


class ChannelRepository(RepositoryBase):
    """Repository for DB operations related to ."""

    # TODO modify to accomodate request models instead.
    # def _build_filter_statement(self, table: SQLModel, filter: Filter):
    #     # Get single value filters.
    #     filter_simple = {k: v for k, v in filter.simple.items() if v is not None}
    #     filter_conditions = [
    #         getattr(Channel, key) == value for key, value in filter_simple.items()
    #     ]

    #     query = select(table)
    #     query = query.filter(and_(*filter_conditions))

    #     # Get range filters.
    #     filter_range = None
    #     range_conditions = [
    #         getattr(Channel, key).between(min_value, max_value)
    #         for key, (min_value, max_value) in filter.range_.items()
    #         if min_value is not None and max_value is not None
    #     ]

    #     query = query.filter(and_(*range_conditions))

    def find_channels_by_structure_id(self, session: Session, structure_id: str):
        statement = select(Channel).where(Channel.structure_id == structure_id)
        channels: Channel = session.exec(statement).all()

        tunnels_dict = {}

        return channels

    def find_channels_by_params(self, session: Session, filter: Filter):
        statement = self._build_filter_statement(Channel, filter)
        channels = session.exec(statement).all()
        return channels
