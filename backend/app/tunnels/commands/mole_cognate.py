from xml.etree.ElementTree import SubElement

from app.database.models import Methods
from app.log import log
from app.tunnels.commands.config.cognate_points import POINTS
from app.tunnels.commands.mole_base import MoleTemplate


class MoleCognate(MoleTemplate):
    TUNNEL_TYPE = "cognate"
    METHOD_ID = Methods.PROCOGNATE_TUNNELS_MOLE

    def configure(self, protein: str) -> None:
        """Creates configuration file for Mole software.

        Args:
            protein: name of protein
        """
        log.debug(
            f"WORKER {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Creating XML configuration file for {protein}."
        )

        try:
            coordinates = POINTS[protein.lower()]
        except KeyError:
            log.debug(
                f"WORKER {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Protein {protein} has no cognate points."
            )
            raise KeyError()
        coords_dict = {"X": coordinates[0], "Y": coordinates[1], "Z": coordinates[2]}

        origin = self.new_xml.getroot().find("./Origins/Origin")
        SubElement(origin, "Point", attrib=coords_dict)

        self._finalize_configuration(protein)

        log.debug(
            f"WORKER {self.worker_id} {self.TUNNEL_TYPE.upper()} -- Configuration file created."
        )
