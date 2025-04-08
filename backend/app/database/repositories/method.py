from sqlmodel import insert, select
from app.database.repositories.base import RepositoryBase
from app.database.models import Method, Methods

from app.log import logger as log


METHODS_NAMES = {
    Methods.CSA_TUNNELS_MOLE: "CSATunnels_MOLE",
    Methods.CSA_TUNNELS_CAVER: "CSATunnels_Caver",
    Methods.REVIEWED_CHANNELS_MOLE: "ReviewedChannels_MOLE",
    Methods.REVIEWED_CHANNELS_CAVER: "ReviewedChannels_Caver",
    Methods.COFACTOR_TUNNELS_MOLE: "CofactorTunnels_MOLE",
    Methods.COFACTOR_TUNNELS_CAVER: "CofactorTunnels_Caver",
    Methods.TRANSMEMBRANE_PORES_MOLE: "TransmembranePores_MOLE",
    Methods.TRANSMEMBRANE_PORES_CAVER: "TransmembranePores_Caver",
    Methods.PROCOGNATE_TUNNELS_MOLE: "ProcognateTunnels_MOLE",
    Methods.PROCOGNATE_TUNNELS_CAVER: "ProcognateTunnels_Caver",
    Methods.ALPHAFILL_TUNNELS_MOLE: "AlphaFillTunnels_MOLE",
    Methods.ALPHAFILL_TUNNELS_CAVER: "AlphaFillTunnels_Caver",
}


class MethodRepository(RepositoryBase):

    def init_table(self):
        statement = select(Method.id, Method.name)

        result = self.db.exec(statement).all()

        if result:
            log.debug(
                f"Methods table is not empty, skipping initialization. Present methods: {result}"
            )
            return False

        values = [
            {"id": method.value, "name": METHODS_NAMES[method]} for method in Methods
        ]
        statement = insert(Method).values(values)

        result = self.db.exec(statement)
        self.db.commit()
        log.debug(f"Inserted predefined methods: {values}")

        return True
