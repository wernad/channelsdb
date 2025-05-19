from app.database.models.annotation import (
    Annotation,
    AnnotationOutput,
    AnnotationsOutput,
    AnnotationInsert,
)

from app.database.models.channel import (
    Channel,
    ChannelInsert,
    ChannelOutput,
    ChannelsResponse,
    ChannelFilter,
)

from app.database.models.het_residue import HetResidue, HetResidueInsert
from app.database.models.layer import (
    Layer,
    LayerGeometry,
    LayerInfo,
    LayerInsert,
    LayerProperties,
    Layers,
)
from app.database.models.layer_residue import LayerResidue, LayerResidueInsert
from app.database.models.method import (
    METHODS_IDS_TO_NAMES,
    Method,
    Methods,
    METHODS_NAMES_TO_IDS,
)
from app.database.models.profile import Profile, ProfileInsert, ProfileOutput
from app.database.models.residue import (
    RESIDUE_NAME_TO_ID,
    RESIDUES_VALUES,
    Residue,
    Residues,
)
from app.database.models.source import Source, Sources
from app.database.models.structure import Structure, StructureData, StructureInsert

ChannelOutput.model_rebuild()
ChannelsResponse.model_rebuild()
