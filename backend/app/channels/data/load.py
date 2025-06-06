"""Wraps run methods for given load approach (JSON, remote database, mirror database)"""

from app.log import log
from app.channels.data.loaders import run_file, run_mirror, run_remote


def load_from_pdb(start: int, fetch_source: str, skip_existing: bool) -> None:
    """Starts loading proteins from PDB database. User can specify mirror or remote

    Args:
        start: what index to start at.
        fetch_source: Type of PDB database to use.
        skip_existing: If existing structures should be skipped.
    """

    log.debug(f"Starting protein loading from '{fetch_source}' PDB database.")
    if fetch_source == "remote":
        run_remote(start=start, skip_existing=skip_existing)
    else:
        run_mirror(start=start, skip_existing=skip_existing)


def load_from_file(file_path: str, skip_existing: bool) -> None:
    """Loads JSON file from given JSON file path.

    Args:
        file_path: Path to JSON file.
        skip_existing: If existing structures should be skipped.
    """

    log.debug(f"Starting protein loading from local file: {file_path}.")
    run_file(file_path, skip_existing=skip_existing)
