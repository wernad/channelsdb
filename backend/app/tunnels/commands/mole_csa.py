from app.database.models import Methods
from app.log import log
from app.tunnels.commands.mole_base import MoleTemplate


class MoleCSA(MoleTemplate):
    TUNNEL_TYPE = "csa"
    METHOD_ID = Methods.CSA_TUNNELS_MOLE

    def configure(self, protein: str) -> None:
        """Creates configuration file for Mole software.

        Args:
            protein: name of protein
        """
        log.debug(
            f"Worker {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Creating XML configuration file for {protein}.."
        )
        self._finalize_configuration(protein)

        log.debug(
            f"Worker {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Configuration file created."
        )
