from sqlmodel import SQLModel, Session, and_, select

from app.database.models import Channel, Annotation
from app.database.common import Filter


def _build_filter_statement(table: SQLModel, filter: Filter):
    # Get single value filters.
    filter_simple = {k: v for k, v in filter.simple.items() if v is not None}
    filter_conditions = [
        getattr(Channel, key) == value for key, value in filter_simple.items()
    ]

    query = select(table)
    query = query.filter(and_(*filter_conditions))

    # Get range filters.
    range_conditions = [
        getattr(Channel, key).between(min_value, max_value)
        for key, (min_value, max_value) in filter.range_.items()
        if min_value is not None and max_value is not None
    ]

    query = query.filter(and_(*range_conditions))


def find_channels_by_structure_id(session: Session, structure_id: str):
    statement = select(Channel).where(Channel.structure_id == structure_id)
    tunnels = session.exec(statement).all()
    return tunnels


def find_channels_by_params(session: Session, filter: Filter):
    statement = _build_filter_statement(Channel, filter)
    channels = session.exec(statement).all()
    return channels


def find_annotations_by_channel_id(session: Session, channel_id: int):
    statement = select(Annotation).where(Annotation.channel_id == channel_id)
    annotations = session.exec(statement).all()
    return annotations
