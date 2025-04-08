from sqlmodel import insert, select
from app.database.repositories.base import RepositoryBase
from app.database.models import Residue, Residues

from app.log import logger as log


RESIDUES_VALUES = {
    Residues.ALA: {
        "name": "ala",
        "charge": 0,
        "hydropathy": 1.8,
        "hydrophobicity": 0.02,
        "polarity": 0,
        "mutability": 100,
    },
    Residues.ARG: {
        "name": "arg",
        "charge": 1,
        "hydropathy": -4.5,
        "hydrophobicity": -0.42,
        "polarity": 52,
        "mutability": 83,
    },
    Residues.ASN: {
        "name": "asn",
        "charge": 0,
        "hydropathy": -3.5,
        "hydrophobicity": -0.77,
        "polarity": 3.38,
        "mutability": 104,
    },
    Residues.ASP: {
        "name": "asp",
        "charge": -1,
        "hydropathy": -3.5,
        "hydrophobicity": 1.04,
        "polarity": 49.7,
        "mutability": 86,
    },
    Residues.CYS: {
        "name": "cys",
        "charge": 0,
        "hydropathy": 2.5,
        "hydrophobicity": 0.77,
        "polarity": 1.48,
        "mutability": 44,
    },
    Residues.GLU: {
        "name": "glu",
        "charge": -1,
        "hydropathy": -3.5,
        "hydrophobicity": -1.1,
        "polarity": 49.9,
        "mutability": 77,
    },
    Residues.GLN: {
        "name": "gln",
        "charge": 0,
        "hydropathy": -3.5,
        "hydrophobicity": -1.14,
        "polarity": 3.53,
        "mutability": 84,
    },
    Residues.GLY: {
        "name": "gly",
        "charge": 0,
        "hydropathy": -0.4,
        "hydrophobicity": -0.8,
        "polarity": 0,
        "mutability": 50,
    },
    Residues.HIS: {
        "name": "his",
        "charge": 0,
        "hydropathy": -3.2,
        "hydrophobicity": 0.26,
        "polarity": 51.6,
        "mutability": 91,
    },
    Residues.ILE: {
        "name": "ile",
        "charge": 0,
        "hydropathy": 4.5,
        "hydrophobicity": 1.81,
        "polarity": 0.13,
        "mutability": 103,
    },
    Residues.LEU: {
        "name": "leu",
        "charge": 0,
        "hydropathy": 3.8,
        "hydrophobicity": 1.14,
        "polarity": 0.13,
        "mutability": 54,
    },
    Residues.LYS: {
        "name": "lys",
        "charge": 1,
        "hydropathy": -3.9,
        "hydrophobicity": -0.41,
        "polarity": 49.5,
        "mutability": 72,
    },
    Residues.MET: {
        "name": "met",
        "charge": 0,
        "hydropathy": 1.9,
        "hydrophobicity": 1.0,
        "polarity": 1.43,
        "mutability": 93,
    },
    Residues.PHE: {
        "name": "phe",
        "charge": 0,
        "hydropathy": 2.8,
        "hydrophobicity": 1.35,
        "polarity": 0.35,
        "mutability": 51,
    },
    Residues.PRO: {
        "name": "pro",
        "charge": 0,
        "hydropathy": -1.6,
        "hydrophobicity": -0.09,
        "polarity": 1.58,
        "mutability": 58,
    },
    Residues.SER: {
        "name": "ser",
        "charge": 0,
        "hydropathy": -0.8,
        "hydrophobicity": -0.97,
        "polarity": 1.67,
        "mutability": 117,
    },
    Residues.THR: {
        "name": "thr",
        "charge": 0,
        "hydropathy": -0.7,
        "hydrophobicity": -0.77,
        "polarity": 1.66,
        "mutability": 107,
    },
    Residues.TRP: {
        "name": "trp",
        "charge": 0,
        "hydropathy": -0.9,
        "hydrophobicity": 1.71,
        "polarity": 2.1,
        "mutability": 25,
    },
    Residues.TYR: {
        "name": "tyr",
        "charge": 0,
        "hydropathy": -1.3,
        "hydrophobicity": 1.11,
        "polarity": 1.61,
        "mutability": 50,
    },
    Residues.VAL: {
        "name": "val",
        "charge": 0,
        "hydropathy": 4.2,
        "hydrophobicity": 1.13,
        "polarity": 0.13,
        "mutability": 98,
    },
}


class ResidueRepository(RepositoryBase):

    def init_table(self):
        statement = select(Residue.id, Residue.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Residues table is not empty, skipping initialization. Present residues: {result}"
            )
            return False

        values = [
            {"id": residue.value, **RESIDUES_VALUES[residue]} for residue in Residues
        ]
        statement = insert(Residue).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined residues: {values}")
        return True
