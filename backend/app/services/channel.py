"""Service module for managing protein channels.

This module provides the ChannelService class for handling business logic related to
protein channels, including retrieving channel data, formatting channel information,
and inserting new channels in bulk or individually.
"""

from statistics import mean

from sqlmodel import Session

from app.database.models import (
    METHODS_IDS_TO_NAMES,
    Channel,
    ChannelInsert,
    ChannelOutput,
    LayerGeometry,
    LayerInfo,
    LayerProperties,
    Layers,
    ProfileOutput,
)
from app.database.repositories.channel import ChannelRepository


class ChannelService:
    """Service for managing protein channels.

    This class provides methods for retrieving and formatting channel data, including
    layer information, residue properties, and geometric measurements. It also handles
    channel insertions and acts as a business logic layer between the API and the
    database repository.
    """

    repository: ChannelRepository

    def __init__(self, db: Session):
        """Initialize the ChannelService with a database session.

        Args:
            db: SQLModel database session for database operations.
        """
        self.repository = ChannelRepository(db)

    @staticmethod
    def channels_with_as_model(channels: list["Channel"]) -> dict:
        """Formats channel data into a structured dictionary.

        Processes channel data to include method-specific information, profiles,
        layer geometries, and residue properties. Calculates various statistics
        for each layer including charge, hydrophobicity, and mutability.

        Args:
            channels: List of Channel objects to format.

        Returns:
            Dictionary mapping method names to lists of formatted ChannelOutput objects,
            each containing detailed information about the channel's properties and layers.
        """
        result = {}

        for channel in channels:
            method = channel.method.name
            if method not in result:
                result[method] = []
            result[method].append(
                ChannelOutput(
                    type=channel.type,
                    id=f"{channel.id}",
                    cavity=f"{channel.cavity}",
                    auto=channel.auto,
                    profile=[ProfileOutput(**dict(p)) for p in channel.profiles],
                    layers=Layers(
                        residue_flow=[
                            f"{lr.residue.name.upper() if lr.residue else 'unknown'} {lr.sequence_number} {lr.chain_id}{' Backbone' if lr.backbone else ''}"
                            for layer in channel.layers
                            for lr in sorted(
                                layer.layer_residues, key=lambda x: x.flow_id
                            )
                        ],
                        het_residues=[
                            f"{hr.residue.name.upper() if hr.residue else 'unknown'} {hr.sequence_number} {hr.chain_id}{' Backbone' if hr.backbone else ''}"
                            for hr in channel.het_residues
                        ],
                        layers_info=[
                            LayerInfo(
                                layer_geometry=LayerGeometry(
                                    radius=layer.radius,
                                    free_radius=layer.free_radius,
                                    start_distance=layer.start_distance,
                                    end_distance=layer.end_distance,
                                    local_minimum=layer.local_minimum,
                                    bottleneck=layer.bottleneck,
                                ),
                                residues=list(
                                    set(
                                        [
                                            f"{lr.residue.name.upper() if lr.residue else 'unknown'} {lr.sequence_number} {lr.chain_id}{' Backbone' if lr.backbone else ''}"
                                            for lr in sorted(
                                                layer.layer_residues,
                                                key=lambda lr: lr.flow_id,
                                            )
                                        ]
                                    )
                                ),
                                properties=LayerProperties(
                                    charge=sum(
                                        lr.residue.charge if lr.residue else 0
                                        for lr in layer.layer_residues
                                    ),
                                    num_positives=len(
                                        [
                                            (
                                                lr.residue.charge
                                                if lr.residue and lr.residue.charge > 0
                                                else 0
                                            )
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                    num_negatives=len(
                                        [
                                            (
                                                lr.residue.charge
                                                if lr.residue and lr.residue.charge < 0
                                                else 0
                                            )
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                    hydrophobicity=mean(
                                        [
                                            (
                                                lr.residue.hydrophobicity
                                                if lr.residue
                                                else 0
                                            )
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                    hydropathy=mean(
                                        [
                                            lr.residue.hydropathy if lr.residue else 0
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                    polarity=mean(
                                        [
                                            lr.residue.polarity if lr.residue else 0
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                    mutability=mean(
                                        [
                                            lr.residue.mutability if lr.residue else 0
                                            for lr in layer.layer_residues
                                        ]
                                    ),
                                ),
                            )
                            for layer in sorted(
                                channel.layers, key=lambda x: x.layer_order
                            )
                        ],
                    ),
                )
            )
        return result

    def get_channels_with_by_structure_internal_id(
        self, internal_id: str
    ) -> dict | None:
        """Retrieves and formats all channel data for a given structure.

        Args:
            internal_id: Internal ID of the structure.

        Returns:
            Dictionary mapping method names to lists of formatted ChannelOutput objects,
            or None if no channels are found.
        """
        channels = self.repository.get_channels_by_internal_id(internal_id)

        if not channels:
            return None

        formatted_channels = ChannelService.channels_with_as_model(channels)

        for method in METHODS_IDS_TO_NAMES.values():
            if method not in formatted_channels:
                formatted_channels[method] = []

        return formatted_channels

    def insert_in_bulk(self, values: list[ChannelInsert]) -> list[int] | None:
        """Inserts multiple channel records in a single operation.

        Args:
            values: List of ChannelInsert objects containing channel data to insert.

        Returns:
            List of IDs for the newly inserted channels, or None if insertion failed.
        """
        result = self.repository.insert_in_bulk(values)

        if result:
            return result

        return None

    def insert_entry(self, values: ChannelInsert) -> int | None:
        """Inserts a single channel record.

        Args:
            values: ChannelInsert object containing the channel data to insert.

        Returns:
            ID of the newly inserted channel, or None if insertion failed.
        """
        result = self.repository.insert_entry(values=values)

        if result:
            return result

        return None
