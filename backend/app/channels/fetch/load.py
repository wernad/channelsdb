from app.log import log
from app.channels.fetch.loaders import pdb, from_file


def load_from_pdb(start: int, fetch_source: str) -> None:
    """Starts loading proteins from PDB database. User can specify mirror or remote

    Args:
        fetch_source: type of PDB database to use.
    """

    log.debug(f"Starting protein loading from '{fetch_source}' PDB database.")
    if fetch_source == "remote":
        pdb.run(start=start)
    else:  # TODO
        ...


def load_from_file(file_path: str) -> None:
    """Loads JSON file from given JSON file path.

    Args:
        file_path: Path to JSON file.
    """

    log.debug(f"Starting protein loading from local file: {file_path}.")
    from_file.run(file_path)
