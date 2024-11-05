from app.database.repositories.channels import ChannelRepository
from app.api.services import ServiceBase


class ChannelService(ServiceBase):
    _repository_class = ChannelRepository
    repository: ChannelRepository

    @staticmethod
    def _get_average(values: list):
        return sum(v for v in values) / len(values)

    # TODO fix residues order per channel.
    # TODO possibly move annotation fetching to its own repo.
    # TODO move ORM to repository.
    def get_channels_by_structure_json(self, structure_id: str):
        """Fetches all necessary data about structure's channels and returns them as a dict."""
        channels = self.repository.get_channels_by_structure_id(structure_id)

        result = {"annotations": [], "channels": {}}
        for channel in channels:
            if channel.annotation:
                result["Annotations"].append(
                    {
                        "Name": channel.annotation.name,
                        "Channel_id": channel.annotation.channel_id,
                        "Description": channel.annotation.description,
                        "Reference": channel.annotation.reference,
                        "Reference_type": channel.annotation.reference_type,
                    }
                )

            if channel.method.name.upper() not in result:
                result["channels"][channel.method.name.upper()] = []

            result["channels"][channel.method.name.upper()].append(
                {
                    "Type": channel.category.name,
                    "Id": channel.id,
                    "Cavity": channel.cavity,
                    "Auto": channel.auto,
                    "Profile": channel.profiles,
                    "Layers": {
                        "ResidueFlow": [
                            f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                            for layer in channel.layers
                            for lr in sorted(layer.layer_residues, key=lambda lr: lr.sequence_number)
                        ],
                        "HetResidues": channel.het_residues,
                        "LayersInfo": [
                            {
                                "LayerGeometry": {
                                    "MinRadius": layer.radius,
                                    "MinFreeRadius": layer.free_radius,
                                    "StartDistance": layer.start_distance,
                                    "EndDistance": layer.end_distance,
                                    "LocalMinimum": layer.local_minimum,
                                    "Bottleneck": layer.bottleneck,
                                },
                                "Residues": [
                                    f"{lr.residue.name.upper()} {lr.sequence_number} {lr.chain_id}{" Backbone" if lr.backbone else ""}"
                                    for lr in sorted(layer.layer_residues, key=lambda lr: lr.flow_id)
                                ],
                                "Properties": {
                                    "Charge": sum(lr.residue.charge for lr in layer.layer_residues),
                                    "NumPositives": len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    "NumNegatives": len(
                                        [lr.residue.charge for lr in layer.layer_residues if lr.residue.charge > 0]
                                    ),
                                    "Hydrophobicity": ChannelService._get_average(
                                        [lr.residue.hydrophobicity for lr in layer.layer_residues]
                                    ),
                                    "Hydropathy": ChannelService._get_average(
                                        [lr.residue.hydropathy for lr in layer.layer_residues]
                                    ),
                                    "Polarity": ChannelService._get_average(
                                        [lr.residue.polarity for lr in layer.layer_residues]
                                    ),
                                    "Mutability": ChannelService._get_average(
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
