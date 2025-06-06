"""Repository module for managing channel layers.

This module provides the LayerRepository class for database operations related to
channel layers, including retrieving layer statistics and inserting new layers
in bulk or individually.
"""

from sqlmodel import insert, select, func, case

from app.database.models import Layer, LayerInsert, Channel, Structure
from app.database.repositories.base import RepositoryBase
from app.log import log


class LayerRepository(RepositoryBase):
    """Repository for managing channel layers.

    This class provides methods for retrieving layer statistics (such as length
    and bottleneck radius statistics) and inserting new layers into the database.
    """

    def get_length_statistics(self) -> dict:
        """Returns statistics about channel lengths.

        Calculates mean, median, minimum, maximum, and standard deviation of
        channel lengths based on layer end distances.

        Returns:
            Dictionary containing statistical measures of channel lengths.
        """
        log.debug("Building length statistics result.")
        cte_statement = (
            select(Structure.external_id, func.max(Layer.end_distance).label("length"))
            .select_from(Layer)
            .join(Channel, Channel.id == Layer.channel_id)
            .join(Structure, Structure.id == Channel.structure_id)
            .group_by(Structure.external_id)
            .cte("channel_lengths")
        )

        min_length_subq = select(func.min(cte_statement.c.length)).scalar_subquery()
        max_length_subq = select(func.max(cte_statement.c.length)).scalar_subquery()

        statement = select(
            func.avg(cte_statement.c.length).label("avg"),
            func.min(cte_statement.c.length).label("min"),
            func.max(cte_statement.c.length).label("max"),
            func.percentile_cont(0.5)
            .within_group(cte_statement.c.length)
            .label("median"),
            func.stddev(cte_statement.c.length).label("stdev"),
            func.max(
                case(
                    (
                        cte_statement.c.length == min_length_subq,
                        cte_statement.c.external_id,
                    ),
                    else_=None,
                )
            ).label("min_structure_id"),
            func.max(
                case(
                    (
                        cte_statement.c.length == max_length_subq,
                        cte_statement.c.external_id,
                    ),
                    else_=None,
                )
            ).label("max_structure_id"),
        ).select_from(cte_statement)

        result = self.db.exec(statement).mappings().first()

        return result

    def get_bottleneck_radius_statistics(self) -> dict:
        """Returns statistics about channel bottleneck radii.

        Calculates mean, median, minimum, maximum, and standard deviation of
        channel bottleneck radii.

        Returns:
            Dictionary containing statistical measures of bottleneck radii.
        """
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
        """Inserts multiple layer records in a single database operation.

        Args:
            values: List of LayerInsert objects to insert.

        Returns:
            List of IDs for the newly inserted layers.
        """
        values = [value.model_dump() for value in values]
        statement = insert(Layer).values(values).returning(Layer.id)
        result = self.db.exec(statement)

        ids = [id[0] for id in result.all()]

        return ids

    def insert_entry(self, values: LayerInsert) -> int:
        """Inserts a single layer record.

        Args:
            values: LayerInsert object containing the layer data.

        Returns:
            ID of the newly inserted layer.
        """
        statement = insert(Layer).values(values.model_dump()).returning(Layer.id)
        result = self.db.exec(statement)
        self.db.commit()

        id = result.first()
        if id:
            id = id[0]
        return id
