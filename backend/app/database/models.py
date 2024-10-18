from sqlmodel import Field, SQLModel, Relationship, JSON


class Annotation(SQLModel, table=True):
    id: float
    structure_id: int
    name: str
    description: str
    reference: str
    referenceType: str


class Channels(SQLModel):
    annotations: list[Annotation]
    channels: list["Channel"]


class Channel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    structure_id: int
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")
    auto: bool

    method: "Method" = Relationship(back_populates="channels")
    category: "Category" = Relationship(back_populates="channels")
    layers: list["Layer"] = Relationship(cascade_delete=True, back_populates="channel")
    het_residues: list["HetResidue"] = Relationship(back_populates="channel")


class Method(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    channels: list["Channel"] = Relationship(back_populates="method")


class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    channels: list["Channel"] = Relationship(back_populates="category")


class Layer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")
    order: int
    radius: float
    free_radius: float
    start_distance: float
    end_distance: float
    local_minimum: bool
    bottleneck: bool

    channel: Channel = Relationship(back_populates="layers")
    residues: list["LayerResidue"] = Relationship(back_populates="layer")


class Residue(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    charge: int = Field(index=True)
    hodropathy: float = Field(index=True)
    polarity: float = Field(index=True)
    mutability: int = Field(index=True)

    layers: list["LayerResidue"] = Relationship(back_populates="residue")


class HetResidue(SQLModel, table=True):
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    channel_id: int = Field(primary_key=True, foreign_key="channel.id")
    sequence_number: int
    type: str

    channel: Channel = Relationship(back_populates="channel")


class LayerResidue(SQLModel, table=True):
    layer_id: int = Field(primary_key=True, foreign_key="layers.id")
    residue_id: int = Field(primary_key=True, foreign_key="residue.id")
    sequence_number: int
    type: str
    flow_id: int
    coord_x: float
    coord_y: float
    coord_z: float
    backbone: bool

    layer: Layer = Relationship(back_populates="residues")
    residue: Residue = Relationship(back_populates="layers")


class Profile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    channel_id: int = Field(foreign_key="channel.id")
    radius: float
    free_radius: float
    t_value: float
    coord_x: float
    coord_y: float
    coord_z: float
    distance: float
    charge: float


# TODO not used yet
class ConfigFile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    config_file: JSON
