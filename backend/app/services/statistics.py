from datetime import datetime as dt

from sqlmodel import Session
from app.database.repositories.channels import ChannelRepository


class StatisticsService:
    repository: ChannelRepository

    def __init__(self, db: Session):
        self.repository = ChannelRepository(db)

    def get_channel_counts_by_software_method(self) -> dict:
        result = self.repository.get_channel_counts_by_software_method()

        date = dt.now().date()
        if result:
            entries_count = sum(row.count for row in result)
            entries = {f"{row.label}_{row.software}": row.count for row in result}
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
