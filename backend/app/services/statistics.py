from datetime import datetime as dt

from sqlmodel import Session

from app.database.models import METHODS_NAMES
from app.database.repositories.channel import ChannelRepository


class StatisticsService:
    repository: ChannelRepository

    def __init__(self, db: Session):
        self.repository = ChannelRepository(db)

    def get_channel_counts_per_category(self) -> dict:
        result = self.repository.get_channel_counts_per_category()

        date = dt.now().date()
        if result:
            entries_count = sum(row.count for row in result)
            entries = {f"{row.method}": row.count for row in result}
            result = {
                "date": date,
                "entries_count": entries_count,
                "statistics": entries,
            }
        else:
            result = {
                "date": date,
                "entries_count": 0,
                "statistics": {},
            }

        return result

    def get_channel_counts_by_id(self, structure_id: int) -> dict:
        result = self.repository.get_channel_counts_by_id(structure_id=structure_id)

        date = dt.now().date()
        if result:
            entries_count = sum(row.count for row in result)
            entries = {method: 0 for method in METHODS_NAMES.values()}
            for row in result:
                entries[row.method] = row.count

            result = {
                "date": date,
                "entries_count": entries_count,
                "statistics": entries,
            }
        else:
            result = {
                "date": date,
                "entries_count": 0,
                "statistics": {},
            }

        return result
