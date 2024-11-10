from sqlmodel import Session
from app.database.repositories.channels import ChannelRepository


class ChannelService:
    repository: ChannelRepository

    def __init__(self, db: Session):
        self.repository = ChannelRepository(db)

    @staticmethod
    def _get_average(values: list):
        return sum(v for v in values) / len(values)

    # TODO fix residues order per channel.
    def get_channels_by_structure_json(self, structure_id: str):
        """Fetches all necessary data about structure's channels and returns them as a dict."""
        channels = self.repository.get_channels_by_structure_id(structure_id)

        result = {}

        for channel in channels:
            method = channel.method.name.upper()
            if method not in result:
                result[method] = []

            result[method].append(
                {
                    "type": channel.category.name,
                    "id": channel.id,
                    "cavity": channel.cavity,
                    "auto": channel.auto,
                    "profile": channel.profiles,
                    "layers": {
                        "residueFlow": [
                            f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                            for layer in channel.layers
                            for lr in sorted(layer.layer_residues, key=lambda lr: lr.sequence_number)
                        ],
                        "hetResidues": channel.het_residues,
                        "layersInfo": [
                            {
                                "layerGeometry": {
                                    "minRadius": layer.radius,
                                    "minFreeRadius": layer.free_radius,
                                    "startDistance": layer.start_distance,
                                    "endDistance": layer.end_distance,
                                    "localMinimum": layer.local_minimum,
                                    "bottleneck": layer.bottleneck,
                                },
                                "residues": [
                                    f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                                    for lr in sorted(layer.layer_residues, key=lambda lr: lr.flow_id)
                                ],
                                "properties": {
                                    "charge": sum(lr.residue.charge for lr in layer.layer_residues),
                                    "numPositives": len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    "numNegatives": len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    "hydrophobicity": ChannelService._get_average(
                                        [lr.residue.hydrophobicity for lr in layer.layer_residues]
                                    ),
                                    "hydropathy": ChannelService._get_average(
                                        [lr.residue.hydropathy for lr in layer.layer_residues]
                                    ),
                                    "polarity": ChannelService._get_average(
                                        [lr.residue.polarity for lr in layer.layer_residues]
                                    ),
                                    "mutability": ChannelService._get_average(
                                        [lr.residue.mutability for lr in layer.layer_residues]
                                    ),
                                },
                            }
                            for layer in channel.layers
                        ],
                    },
                }
            )

        return result
