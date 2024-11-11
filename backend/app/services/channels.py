from typing import TYPE_CHECKING

from sqlmodel import Session
from app.database.repositories.channels import ChannelRepository

if TYPE_CHECKING:
    from app.database.models import (
        Channel,
        ChannelOutput,
        ProfileOutput,
        Layers,
        LayerInfo,
        LayerGeometry,
        LayerProperties,
    )


class ChannelService:
    repository: ChannelRepository

    def __init__(self, db: Session):
        self.repository = ChannelRepository(db)

    @staticmethod
    def _get_average(values: list):
        return sum(v for v in values) / len(values)

    @staticmethod
    def channels_with_annotations_as_model(channels: list[Channel]) -> dict:
        result = {}

        for channel in channels:
            method = channel.method.name.upper()
            if method not in result:
                result[method] = []

            result[method].append(
                ChannelOutput(
                    type=channel.category.name,
                    id=channel.id,
                    cavity=channel.cavity,
                    auto=channel.auto,
                    profile=[ProfileOutput(**p) for p in channel.profiles],
                    layers=Layers(
                        residue_flow=[
                            f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                            for layer in channel.layers
                            for lr in sorted(layer.layer_residues, key=lambda x: x.sequence_number)
                        ],
                        het_residues=[
                            f"{hr.residue.name.upper()} {hr.sequence_number} {hr.chain_id}{" Backbone" if hr.backbone else ""}"
                            for hr in sorted(channel.het_residues, key=lambda x: x.sequence_number)
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
                                            f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                                            for lr in sorted(layer.layer_residues, key=lambda lr: lr.sequence_number)
                                        ]
                                    )
                                ),
                                properties=LayerProperties(
                                    charge=sum(lr.residue.charge for lr in layer.layer_residues),
                                    num_positives=len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    num_negatives=len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    hydrophobicity=ChannelService._get_average(
                                        [lr.residue.hydrophobicity for lr in layer.layer_residues]
                                    ),
                                    hydropathy=ChannelService._get_average(
                                        [lr.residue.hydropathy for lr in layer.layer_residues]
                                    ),
                                    polarity=ChannelService._get_average(
                                        [lr.residue.polarity for lr in layer.layer_residues]
                                    ),
                                    mutability=ChannelService._get_average(
                                        [lr.residue.mutability for lr in layer.layer_residues]
                                    ),
                                ),
                            )
                            for layer in sorted(channel.layers, key=lambda x: x.layer_order)
                        ],
                    ),
                )
            )
        return result

    # TODO fix residues order in channels.
    def get_channels_with_annotations_by_structure(self, structure_id: str):
        """Fetches all necessary data about structure's channels and returns them as a dict."""
        channels = self.repository.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        return ChannelService.channels_with_annotations_as_model(channels)
