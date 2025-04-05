from sqlmodel import func, select, join

from app.database.repositories.base import RepositoryBase
from app.database.models import Channel, Category, Method
from app.database.structures import Filter


# TODO possibly add services to handle manipulation of fetched data.
# TODO potentially change engine and repo to true async
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

    def get_channels_by_structure_id(self, structure_id: str) -> list[Channel]:
        statement = select(Channel).where(Channel.structure_id == structure_id)
        channels = self.db.exec(statement).all()

        return channels

    def get_channels_by_params(self, filter: Filter):
        statement = self._build_filter_statement(Channel, filter)
        channels = self.db.exec(statement).all()
        return channels

    def get_channel_counts_per_category(self) -> list[tuple]:
        statement = (
            select(
                Category.name.label("category"),
                Method.name.label("method"),
                func.count(Channel.id).label("count"),
            )
            .join(Channel, Channel.method_id == Method.id)
            .group_by(Method.name, Category.name)
            .order_by(func.count(Channel.id).desc())
        )

        counts = self.db.exec(statement)

        return counts

    def get_channel_counts_by_id(self, structure_id: str) -> list[tuple]:
        statement = (
            select(
                Category.name.label("category"),
                Method.name.label("method"),
                func.count(Channel.id).label("count"),
            )
            .join(Channel, Channel.method_id == Method.id)
            .group_by(Method.name, Category.name)
            .where(Channel.structure_id == structure_id)
            .order_by(func.count(Channel.id).desc())
        )

        counts = self.db.exec(statement)

        return counts
