from app.database.models.annotation import (
    Annotation,
    AnnotationOutput,
    AnnotationsOutput,
)
from app.database.models.category import Category
from app.database.models.channel_config import ConfigFile
from app.database.models.het_residue import HetResidue
from app.database.models.layer import (
    Layer,
    Layers,
    LayerInfo,
    LayerGeometry,
    LayerProperties,
)
from app.database.models.layer_residue import LayerResidue
from app.database.models.method import Method
from app.database.models.pdb import PDBData
from app.database.models.profile import Profile, ProfileOutput
from app.database.models.residue import Residue
from app.database.models.channel import Channel, ChannelOutput

ChannelOutput.model_rebuild()
