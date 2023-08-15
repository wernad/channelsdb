from api.common import SourceDatabase
from api.endpoints.channels import get_channels

HEADER = '''\
import chimera, _surface, numpy
from numpy import array, single as floatc, intc

def add_atom(molecule, id, residue, x, y, z, radius):
    at = molecule.newAtom(id, chimera.Element("Tunn"))
    at.setCoord(chimera.Coord(x,y,z))
    at.radius = radius
    residue.addAtom(at)
'''

FOOTER = '''\
channel_object = chimera.Molecule()
channel_object.name = '{name}'
{name}(channel_object)
chimera.openModels.add([channel_object])
'''


def get_Chimera_file(source_db: SourceDatabase, protein_id: str) -> str:
    channels = get_channels(source_db, protein_id)
    channel_count = 0
    lines = []
    for channel_type in channels['Channels']:
        for channel in channels['Channels'][channel_type]:
            channel_count += 1
            name = f'channel{channel_count}'
            lines.append(f'def {name}(channel_object):')
            lines.append(f'    channel = channel_object.newResidue(\'{name}\', \'\', 1, \'\')')
            profile = channel['Profile']
            for current_atom_id, atom in enumerate(profile):
                line = (f'    add_atom(channel_object, \'{name}\', channel, '
                        f'{atom["X"]:.3f}, {atom["Y"]:.3f}, {atom["Z"]:.3f}, {atom["Radius"]:.3f})')
                lines.append(line)

            lines.append(FOOTER.format(name=name))

    return HEADER + '\n'.join(lines) + '\n'
