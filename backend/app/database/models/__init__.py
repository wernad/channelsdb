from app.database.models.annotation import (Annotation, AnnotationOutput,
                                            AnnotationsOutput)
from app.database.models.category import (CATEGORIES_ID_TO_NAME,
                                          CATEGORIES_NAME_TO_ID, Categories,
                                          Category)
from app.database.models.channel import (Channel, ChannelInsert, ChannelOutput,
                                         ChannelsResponse)
# from app.database.models.channel_config import ConfigFile
from app.database.models.het_residue import HetResidue, HetResidueInsert
from app.database.models.layer import (Layer, LayerGeometry, LayerInfo,
                                       LayerInsert, LayerProperties, Layers)
from app.database.models.layer_residue import LayerResidue, LayerResidueInsert
from app.database.models.method import METHODS_NAMES, Method, Methods
from app.database.models.profile import Profile, ProfileInsert, ProfileOutput
from app.database.models.residue import (RESIDUE_NAME_TO_ID, RESIDUES_VALUES,
                                         Residue, Residues)
from app.database.models.source import Source, Sources
from app.database.models.structure import (Structure, StructureData,
                                           StructureInsert)

ChannelOutput.model_rebuild()
ChannelsResponse.model_rebuild()
