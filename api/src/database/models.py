from sqlalchemy import Column, ForeignKey, Integer, Float, String, JSON
from sqlalchemy.orm import relationship

from .database import Base

class Tunnel(Base):
    __tablename__ = "tunnels"

    id = Column(Integer, primary_key=True)
    structure_id = Column(Integer)
    charge_min = Column(Float)
    charge_max = Column(Float)
    hydrophobicity_min = Column(Float)
    hydrophobicity_max = Column(Float)
    hydropathy_min = Column(Float)
    hydropathy_max = Column(Float)
    polarity_min = Column(Float)
    polarity_max = Column(Float)
    mutability_min = Column(Float)
    mutability_max = Column(Float)

    layers = relationship("Layer", back_populates="tunnel")

class TunnelCategory(Base):
    __tablename__ = "tunnel_categories"

    category_id = Column(Integer, ForeignKey("categories.id"))
    tunnel_id = Column(Integer, ForeignKey("tunnels.id"))


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Layer(Base):
    __tablename__ = "layers"
    id = Column(Integer, primary_key=True)
    tunnel_id = Column(Integer, ForeignKey("tunnels.id"))
    order = Column(Integer)
    radius = Column(Float)

    tunnel = relationship("Tunnel", back_populates="layers")
    residues = relationship("Residue", back_populates="layer")

class LayerResidue(Base):
    __tablename__ = "layer_residues"

    layer_id = Column(Integer, ForeignKey("layers.id"))
    residue_id = Column(Integer, ForeignKey("residues.id"))


class Residue(Base):
    __tablename__ = "residues"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    layer_id = Column(Integer, ForeignKey("layers.id"))
    charge = Column(Float)
    Hydropathy = Column(Float)
    Polarity = Column(Float)
    Mutability = Column(Integer)

    layer = relationship("Layer", back_populates="residues")

class ConfigFile(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    config_file = Column(JSON)