from pydantic import BaseModel
from typing import Dict, Any
from channelsdb.api.src.database.models import Layer

    
class TunnelBase(BaseModel):
    structure_id: int
    layers: list[Layer]

class Tunnel(BaseModel):
    id: int

    class Config:
        orm_mode = True


class LayerBase(BaseModel):
    order: int
    tunnel_id: int

class Layer(LayerBase):
    id: int

    class Config:
        orm_mode = True

class LayerCreate(LayerBase):
    pass 

class LayerResidue(BaseModel):
    layer_id: int
    residue_id: int

    class Config:
        orm_mode = True

class TunnelConfigBase(BaseModel):
    name: str
    config: Dict[str, Any]