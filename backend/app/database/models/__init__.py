from app.database.models.annotation import (
    Annotation,
    AnnotationOutput,
    AnnotationsOutput,
)
from app.database.models.category import Category, Categories
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
from app.database.models.method import Method, Methods
from app.database.models.structure import Structure, StructureData
from app.database.models.source import Source, Sources
from app.database.models.profile import Profile, ProfileOutput
from app.database.models.residue import Residue, Residues
from app.database.models.channel import Channel, ChannelOutput, ChannelsResponse

ChannelOutput.model_rebuild()
ChannelsResponse.model_rebuild()
