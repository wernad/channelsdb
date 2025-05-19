"""Contains class for cofactor configuration of Mole software."""

from app.database.models import Methods
from app.log import log
from app.channels.commands.mole_base import MoleTemplate


class MoleCofactor(MoleTemplate):
    """Mole command class for running Mole with cofactor configuration.

    Attributes:
        TUNNEL_TYPE: Type of tunnel to detect.
        METHOD_ID: ID of the method to use.
    """

    TUNNEL_TYPE = "cofactor"
    METHOD_ID = Methods.COFACTOR_TUNNELS_MOLE

    def configure(self, protein: str) -> None:
        """Creates configuration file for Mole software.

        Args:
            protein: name of protein
        """
        log.debug(
            f"WORKER {self.worker_id} {self.TUNNEL_TYPE.upper()}-- Creating XML configuration file for {protein}."
        )
        self._finalize_configuration(protein)

        log.debug(
            f"WORKER {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Configuration file created."
        )
