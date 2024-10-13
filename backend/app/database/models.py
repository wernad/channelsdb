from sqlmodel import Field, SQLModel, Relationship, JSON


# TODO possibly a table ?
class Annotation(SQLModel):
    id: float
    name: str
    description: str
    reference: str
    referenceType: str


class Channels(SQLModel):
    annotations: list[Annotation]
    channels: list["Tunnel"]


class Tunnel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    structure_id: int
    method_id: int = Field(foreign_key="method.id")
    category_id: int = Field(foreign_key="category.id")
    auto: bool

    method: "Method" = Relationship(back_populates="tunnels")
    category: "Category" = Relationship(back_populates="tunnels")
    layers: list["Layer"] = Relationship(cascade_delete=True, back_populates="tunnel")


class Method(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    tunnels: list["Tunnel"] = Relationship(back_populates="method")


class Category(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)

    tunnels: list["Tunnel"] = Relationship(back_populates="category")


class Layer(SQLModel, table=True):
    id: int = Field(primary_key=True)
    tunnel_id: int = Field(foreign_key="tunnel.id")
    order: int
    radius: float
    free_radius: float
    start_distance: float
    end_distance: float
    local_minimum: bool
    bottleneck: bool

    tunnel: Tunnel = Relationship(back_populates="layers")
    residues: list["LayerResidue"] = Relationship(back_populates="layer")


class Residue(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    charge: int = Field(index=True)
    hodropathy: float = Field(index=True)
    polarity: float = Field(index=True)
    mutability: int = Field(index=True)

    layers: list["LayerResidue"] = Relationship(back_populates="residue")


class LayerResidue(SQLModel, table=True):
    layer_id = Field(primary_key=True, foreign_key="layers.id")
    residue_id = Field(primary_key=True, foreign_key="residue.id")
    chain_id: int
    chain_type: int = Field(foreign_key="")
    flow_id: int
    coord_x: float
    coord_y: float
    coord_z: float
    backbone: bool

    layer: Layer = Relationship(back_populates="residues")
    residue: Residue = Relationship(back_populates="layers")


# TODO not used yet
class Profile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    radius: float
    free_radius: float
    t_value: float
    coord_x: float
    coord_y: float
    coord_z: float
    distance: float
    charge: float


# TODO not used yet
class Cavity(SQLModel, table=True):
    id: int = Field(primary_key=True)
    volume: float
    depth: float
    depthLength: float


# TODO not used yet
class ParentType(SQLModel, table=True): ...


# TODO not used yet
class ConfigFile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    config_file: JSON
