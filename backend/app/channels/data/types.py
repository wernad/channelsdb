from app.database.models import (
    ChannelInsert,
    HetResidueInsert,
    LayerInsert,
    LayerResidueInsert,
    ProfileInsert,
    StructureInsert,
)
from app.channels.commands import MoleCofactor, MoleCognate, MoleCSA

MoleClass = MoleCognate | MoleCSA | MoleCofactor
Insertable = (
    StructureInsert
    | ChannelInsert
    | ProfileInsert
    | LayerInsert
    | LayerResidueInsert
    | HetResidueInsert
)
