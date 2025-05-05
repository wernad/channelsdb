from sqlmodel import insert, select, func

from app.database.models import Layer, LayerInsert
from app.database.repositories.base import RepositoryBase
from app.log import log


class LayerRepository(RepositoryBase):
    """Repository for DB operations related to layers."""

    def get_length_statistics(self) -> dict:
        """Returns statistics like mean, median, min, max and standard deviation of channel lengths."""
        log.debug("Building length statistics result.")
        cte_statement = (
            select(Layer.channel_id, func.max(Layer.end_distance).label("length"))
            .group_by(Layer.channel_id)
            .cte("channel_lengths")
        )

        statement = select(
            func.avg(cte_statement.c.length).label("avg"),
            func.min(cte_statement.c.length).label("min"),
            func.max(cte_statement.c.length).label("max"),
            func.percentile_cont(0.5)
            .within_group(cte_statement.c.length)
            .label("median"),
            func.stddev(cte_statement.c.length).label("stdev"),
        )

        result = self.db.exec(statement).mappings().first()

        return result

    def get_bottleneck_radius_statistics(self) -> dict:
        """Returns statistics like mean, median, min, max and standard deviation of channel bottleneck radii."""
        statement = select(
            func.avg(Layer.radius).label("avg"),
            func.min(Layer.radius).label("min"),
            func.max(Layer.radius).label("max"),
            func.percentile_cont(0.5).within_group(Layer.radius).label("median"),
            func.stddev(Layer.radius).label("stdev"),
        ).where(Layer.bottleneck)

        result = self.db.exec(statement).mappings().first()

        return result

    def insert_in_bulk(self, values: list[LayerInsert]) -> list[int]:
        """Inserts new layer rows in bulk."""

        values = [value.model_dump() for value in values]
        statement = insert(Layer).values(values).returning(Layer.id)
        result = self.db.exec(statement)
        self.db.commit()

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: LayerInsert) -> int:
        """Inserts a new layer entry."""

        statement = insert(Layer).values(values.model_dump()).returning(Layer.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
