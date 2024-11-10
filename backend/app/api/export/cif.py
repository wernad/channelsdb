from Bio.PDB.MMCIF2Dict import MMCIF2Dict

MMCIF_ANNOTATION = """
loop_
_annotation.channel_id
_annotation.name
_annotation.description
_annotation.reference
_annotation.reference_type
"""

MMCIF_CHANNEL = """
loop_
_channel.id
_channel.category # Path, Pore, Tunnel, etc
_channel.method # CSATunnel_MOLE, CSATunnel_Caver, etc
_channel.auto # bool
_channel.cavity # integer
"""

MMCIF_LAYER = """
loop_
_layer.id
_layer.channel_id
_layer.order # order in channel
_layer.min_radius
_layer.min_free_radius
_layer.start_distance
_layer.end_distance
_layer.local_minimum # bool
_layer.bottleneck # bool
"""


MMCIF_HET_RESIDUE = """
loop_
_het_residue.channel_id
_het_residue.name
_het_residue.sequence_number
_het_residue.chain_id
"""

MMCIF_RESIDUE_LAYER = """
loop_
_residue_layer.layer_id
_residue_layer.residue_id
_residue_layer.flow
_residue_layer.backbone # bool"""

MMCIF_PROFILE = """
loop_
_profile.channel_id
_profile.radius
_profile.free_radius
_profile.distance
_profile.T
_profile.x
_profile.y
_profile.z
_profile.charge
"""


def get_cif():
    parent_cif = MMCIF2Dict("/home/chiro/Documents/DP/channelsdb/backend/app/api/export/1tqn.cif")
    residue_names = parent_cif["_atom_site.label_comp_id"]
    # id + 1 because cif file starts from index 1.
    name_to_indice = {elem: residue_names.index(elem) + 1 for elem in set(residue_names)}
    print(name_to_indice)
    return parent_cif
