import json
from statistics import mean
from string import ascii_uppercase
from io import BytesIO, StringIO
from zipfile import ZipFile

from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder

from app.services import constants as const, ChannelService
from app.database.repositories.channels import ChannelRepository


class ExportService:
    channel_repo: ChannelRepository

    def __init__(self, db: Session):
        self.channel_repo = ChannelRepository(db)

    @staticmethod
    def name_to_index(content: str):
        """Method loads file with parent CIF and extracts residues with indicies from it based on a key."""
        residue_key = "_atom_site.label_comp_id"
        file = StringIO(content)
        parent_cif = MMCIF2Dict(file)
        residue_names = parent_cif[residue_key]
        # id + 1 because cif file starts from index 1.
        name_to_indices = {
            elem: residue_names.index(elem) + 1 for elem in set(residue_names)
        }

        return name_to_indices

    @staticmethod
    def round_items(values: list[float], decimal_places: int = 3):
        """Round all values to predefined decimal places and joins them into a string."""
        return " ".join(str(round(x, decimal_places)) for x in values)

    def get_json_file(self, structure_id: str) -> str:
        """Creates json file from given channel data using ChannelService."""
        raw = self.channel_repo.get_channels_by_structure_id(structure_id)
        if not raw:
            return None

        channels = ChannelService.channels_with_annotations_as_model(raw)
        json_compatible = jsonable_encoder(channels)
        channels_json = json.dumps(json_compatible)

        return channels_json

    def get_chimera_file(self, structure_id: str) -> str:
        """Builds python that uses chimera package to build required file."""
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        channel_count = 0
        lines = []
        for channels_data in channels.values():
            for channel in channels_data:
                channel_count += 1
                name = f"channel{channel_count}"
                lines.append(f"def {name}(channel_object):")
                lines.append(
                    f"    channel = channel_object.newResidue('{name}', '', 1, '')"
                )
                for atom in channel["profile"]:
                    line = (
                        f"    add_atom(channel_object, '{name}', channel, "
                        f"{atom.coord_x:.3f}, {atom.coord_y:.3f}, {atom.coord_z:.3f}, {atom.free_radius:.3f})"
                    )
                    lines.append(line)

                lines.append(const.CHIMERA_FOOTER.format(name=name))

        for i in range(channel_count):
            lines.append(
                f"chimera.runCommand('color {const.CHIMERA_COLORS[i % len(const.CHIMERA_COLORS)]} #{i + 1}')"
            )
            lines.append(f"chimera.runCommand('repr cpk: {i + 1}')")

        return const.CHIMERA_HEADER + "\n".join(lines) + "\n"

    def get_pdb_file(self, structure_id: str) -> str:
        """Generates a text file using PDB syntax."""
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        total_atom_id = 0
        channel_count = 0
        lines = []
        for channel_type in channels["channels"]:
            for channel in channels["channels"][channel_type]:
                channel_count += 1
                profile = channel["profile"]
                for current_atom_id, atom in enumerate(profile, start=1):
                    total_atom_id += 1
                    line = (
                        f"HETATM{total_atom_id:>5d}  X   TUN {ascii_uppercase[(channel_count - 1) % 26]}{current_atom_id:>4}    "
                        f'{atom["x"]:>8.3f}{atom["y"]:>8.3f}{atom["z"]:>8.3f}'
                        f'{atom["distance"]:>6.2f}{atom["radius"]:>6.3f}'
                    )
                    lines.append(line)

        return const.PDB_HEADER + "\n".join(lines) + "\n"

    def get_pymol_file(self, structure_id: str) -> str:
        """Generates a PyMol string."""
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        channel_count = 0
        lines = []
        for channel_type in channels["channels"]:
            for channel in channels["channels"][channel_type]:
                channel_count += 1
                name = f"channel{channel_count}"
                lines.append(f"def {name}():")
                lines.append("    model = chempy.models.Indexed()")
                profile = channel["profile"]
                for current_atom_id, atom in enumerate(profile):
                    line = f'    add_atom(model, \'{current_atom_id}\', {atom["radius"]:.3f}, {atom["x"]:.3f}, {atom["y"]:.3f}, {atom["z"]:.3f})'
                    lines.append(line)
                lines.append(
                    const.PYMOL_FOOTER.format(
                        name=name,
                        color=const.PYMOL_COLORS[
                            (channel_count - 1) % len(const.PYMOL_COLORS)
                        ],
                    )
                )

        return const.PYMOL_HEADER + "\n".join(lines) + "\n"

    def get_vmd_file(self, structure_id: str) -> str:
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        channel_count = 0
        lines = []
        for channel_type in channels["channels"]:
            for channel in channels["channels"][channel_type]:
                channel_count += 1
                name = f"channel{channel_count}"
                profile = channel["profile"]
                lines.append(
                    const.VMD_CHANNEL_START.format(
                        name=name, num_atoms=len(profile), color_id=channel_count % 33
                    )
                )
                for current_atom_id, atom in enumerate(profile):
                    line = f'add_atom {current_atom_id} {{{{ {atom["x"]:.3f}, {atom["y"]:.3f}, {atom["z"]:.3f} }}}} {atom["radius"]:.3f}'
                    lines.append(line)

                lines.append(const.VMD_CHANNEL_END.format(name=name))
        return const.VMD_HEADER + "\n".join(lines) + "display reset view\n"

    def get_cif_file(self, structure_id: str, file: bytes) -> str:
        """Builds CIF file and inserts it into parent file."""
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)
        decimal_places = 3

        if not channels:
            return None

        file_str = file.decode("utf-8")
        res2idx = ExportService.name_to_index(file_str)

        loops = {
            "annotation": [],
            "channel": [],
            "het_residue": [],
            "layer": [],
            "layer_residue": [],
            "profile": [],
        }
        for channel in channels:
            if channel.annotation:
                loops["annotation"].append(
                    f'{channel.annotation.channel_id} "{channel.annotation.name}" "{channel.annotation.description}" "{channel.annotation.reference}" {channel.annotation.reference_type}'
                )
            method, software = channel.method.name.split("_")
            loops["channel"].append(
                f"{channel.id} {channel.category.name} {method} {software} {channel.auto} {channel.cavity}"
            )

            het_id = len(loops["het_residue"])
            loops["het_residue"].extend(
                [
                    f"{het_id + idx + 1} {res.channel_id} {res.residue.name.upper()} {res.sequence_number} {res.chain_id} {res.backbone}"
                    for idx, res in enumerate(channel.het_residues)
                ]
            )

            profile_id = len(loops["profile"])
            loops["profile"].extend(
                [
                    f"{profile_id + idx + 1} {p.channel_id} {ExportService.round_items([p.radius, p.free_radius,p.distance,p.t_value,p.coord_x, p.coord_y, p.coord_z])} {p.charge}"
                    for idx, p in enumerate(channel.profiles)
                ]
            )

            for layer in channel.layers:
                charge = sum(lr.residue.charge for lr in layer.layer_residues)
                negatives = len(
                    [1 for lr in layer.layer_residues if lr.residue.charge > 0]
                )
                positives = len(
                    [1 for lr in layer.layer_residues if lr.residue.charge < 0]
                )
                hydrophobicity = round(
                    mean([lr.residue.hydrophobicity for lr in layer.layer_residues]),
                    decimal_places,
                )
                hydropathy = round(
                    mean([lr.residue.hydropathy for lr in layer.layer_residues]),
                    decimal_places,
                )
                polarity = round(
                    mean([lr.residue.polarity for lr in layer.layer_residues]),
                    decimal_places,
                )
                mutability = round(
                    mean([lr.residue.mutability for lr in layer.layer_residues]),
                    decimal_places,
                )
                bottleneck = layer.bottleneck if layer.bottleneck else False
                loops["layer"].append(
                    f"{layer.id} {layer.channel_id} {ExportService.round_items([layer.layer_order, layer.radius, layer.free_radius, layer.start_distance, layer.end_distance])} {layer.local_minimum} {bottleneck} {charge} {positives} {negatives} {hydrophobicity} {hydropathy} {polarity} {mutability}"
                )

                loops["layer_residue"].extend(
                    [
                        f"{lr.layer_id} {res2idx[lr.residue.name.upper()]} {lr.flow_id} {lr.backbone}"
                        for lr in layer.layer_residues
                    ]
                )
        result = ""
        loop_headers = [
            const.CIF_ANNOTATION,
            const.CIF_CHANNEL,
            const.CIF_HET_RESIDUE,
            const.CIF_LAYER,
            const.CIF_LAYER_RESIDUE,
            const.CIF_PROFILE,
        ]

        for header, rows in zip(loop_headers, list(loops.values())):
            result += header
            for row in rows:
                result += f"{row}\n"

        result = f"{file_str}\n# CHANNELSDB \n{result}"
        return result

    def get_zip_file(self, structure_id: str):
        """Generate and zip all supported files and return said zip file."""
        channels = self.channel_repo.get_channels_by_structure_id(structure_id)

        if not channels:
            return None

        channels_dict = ChannelService.channels_with_annotations_dict(channels)

        content = BytesIO()
        zf = ZipFile(content, mode="w")
        zf.writestr(f"{structure_id}_chimera.py", self.get_chimera_file(channels))
        zf.writestr(f"{structure_id}_pymol.py", self.get_pymol_file(channels))
        zf.writestr(f"{structure_id}_vmd.tk", self.get_vmd_file(channels))
        zf.writestr(f"{structure_id}_report.json", channels_dict)
        zf.writestr(f"{structure_id}_channels.pdb", self.get_pdb_file(channels))
        zf.close()
