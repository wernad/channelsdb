import json
import os
import shutil
from urllib.parse import quote_plus
import multiprocessing as mp

from requests import Response, get
from requests.exceptions import ConnectTimeout

from app.config import (
    MIRROR_API_PATH,
    OUTPUT_PATH,
    PDB_DATA_API_URL,
    PDB_HTTP_FILE_URL,
    PDB_SEARCH_API_URL,
    QUEUE_SIZE,
)
from app.log import log


def get_full_id(id: str):
    """Returns 12-character id of given 4-character id."""
    return f"pdb_0000{id.lower()}"


def fetch_total_count() -> int:
    """Fetches total number of entires in PDB mirror."""
    api_url = os.environ.get("PDB_MIRROR_API_URL", MIRROR_API_PATH)
    url = f"{api_url}proteins/total_count"

    response = get(url)

    if response.status_code == 200:
        return response.json()["total_count"]


def create_output_directory() -> None:
    """Creates output folder for workers."""
    log.debug("Creating output folder structure.")

    try:
        os.mkdir(OUTPUT_PATH)
        log.debug("Directory created successfully.")
    except FileExistsError:
        print("####", OUTPUT_PATH)
        # shutil.rmtree(OUTPUT_PATH)
        # log.debug(f"Directory '{OUTPUT_PATH}' already exists, cleaning up.")
        # os.mkdir(OUTPUT_PATH)
        log.debug("Directory re-created successfully.")
    except PermissionError:
        log.error(f"Permission denied: Unable to create '{OUTPUT_PATH}'.")
    except Exception as e:
        log.error(f"An error occurred: {e}")


def get_error_message(response: Response) -> str:
    """Extracts error message if any given, otherwise returns plain text."""
    log.debug("Extractng error message.")
    try:
        message = response.json()
    except Exception as _:
        message = response.text

    return message


def fetch_ids(start: int, limit: int, remote: bool = True) -> list[str]:
    """Fetches a list of ids based on start and limit.

    Parameters:
        start: sequence start
        limit: number of ids
        remote: if it should use URL for remote or mirror of PDB.
    Return:
        list[str]
    """

    if remote:
        url = get_search_url(start=start, limit=limit)
    else:
        api_url = os.environ.get("PDB_MIRROR_API_URL", MIRROR_API_PATH)
        url = f"{api_url}proteins/all?limit={limit}&offset={start}"
    response = get(url)

    if response.status_code == 200:
        return response.json()

    log.error(f"Received unexpected status code: {response.status_code}")

    return None


def create_queues() -> list[mp.Queue]:
    """Creates queues for data and results."""
    log.debug("MAIN - Creating queues.")
    data_queue = mp.Queue(maxsize=QUEUE_SIZE)
    result_queue = mp.Queue()
    log.debug("MAIN - Queues created.")
    return data_queue, result_queue


def get_file_url(id: str, version: str = None, remote: bool = True) -> str:
    """Create file url based on id and version.

    Parameters:
        id: structure id
        version: version to fetch.
        remote: flag to use remote or mirror pdb.

    Returns:
        tuple of bytes and error code
    """
    log.debug(f"Creating url for file - {id=} {version=}.")
    if remote:
        id = id.lower()
        full_id = get_full_id(id)
        category = id[1:3]
        file_name = f"{full_id}_xyz_v{version}.cif.gz"
        url = f"{PDB_HTTP_FILE_URL}{category}/{full_id}/{file_name}"
    else:
        api_url = os.environ.get("PDB_MIRROR_API_URL", MIRROR_API_PATH)
        url = f"{api_url}files/{id}/latest"
    log.debug(f"Created file url: {url}")
    return url


def get_graphql_query(id: str) -> str:
    """Helper method to create url encoded string for Data API."""
    log.debug(f"Generating GraphQL query string for id {id}")

    query = (
        f'{{entry(entry_id: "{id}"){{pdbx_audit_revision_history{{major_revision}}}}}}'
    )
    encoded = quote_plus(query)

    url = f"{PDB_DATA_API_URL}?query={encoded}"
    return url


def get_search_url(start: int = 0, limit: int = 1000) -> str:
    """Helper method to create a url encoded string for Search API."""
    log.debug(f"Creating search query string with these params: {start=}, {limit=}")
    params = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_accession_info.initial_release_date",
                "operator": "exists",
            },
        },
        "request_options": {"paginate": {"start": start, "rows": limit}},
        "return_type": "entry",
    }

    json_params = json.dumps(params)
    encoded = quote_plus(json_params)
    url = f"{PDB_SEARCH_API_URL}?json={encoded}"
    log.debug(f"URL string created. {url}")
    return url


def get_last_version(id: str) -> int | None:
    """Fetches latest version number of given file ID."""
    log.debug(f"Fetching latest version of a file with ID {id}.")

    url = get_graphql_query(id)
    log.debug(f"Query for {id}: {url}")

    response = get(url)
    if response.status_code == 200:
        body = response.json()
        version = body["data"]["entry"]["pdbx_audit_revision_history"][-1][
            "major_revision"
        ]
        log.debug(f"File {id} - latest version: {version}.")
        return version

    message = get_error_message(response)
    log.debug(f"No version retrieved for id {id} - error: {message}")
    return None


def get_all_versions(id: str) -> set[int]:
    """Fetches all versions of given structure, if any.

    Args:
        id: id of entry.

    Returns:
        version in a set of integers.
    """

    log.debug(f"Fetching all versions of file with ID {id}.")

    query = get_graphql_query(id)

    url = f"{PDB_DATA_API_URL}?query={query}"
    response = get(url)

    if response.status_code == 200:
        body = response.json()
        data = body["data"]["entry"]["pdbx_audit_revision_history"]

        versions = set([x["major_revision"] for x in data])

        log.debug(f"File {id} - versions found: {versions}.")
        return versions

    message = get_error_message(response)
    log.debug(f"No versions retrieved for id {id} - error: {message}")
    return None


def fetch_files(urls: list[str]) -> list[bytes]:
    """Fetches files from given urls.

    Parameters:
        urls: list of urls
    Returns:
        list of bytes
    """
    log.debug(f"Fetching {len(urls)} files.")
    files = []

    for url in urls:
        response = get(url)

        if response.status_code == 200:
            files.append(response.content)
    log.debug("Fetching done.")
    return files


def fetch_file(url: list[str]) -> list[bytes]:
    """Fetches files from given urls.

    Parameters:
        urls: list of urls
    Returns:
        list of bytes
    """
    log.debug(f"Fetching file from url: {url}")
    finished = False
    while not finished:
        try:
            response = get(url)
            code = response.status_code
            if code == 200:
                log.debug("Fetching complete.")
                finished = True
                return response.content
            log.error(f"Unexpected status code {code} for url: {url}")
        except ConnectTimeout as _:
            log.error(f"Connection timed out on url: {url}")

    log.error(f"Fetching failed for url: {url}")


def fetch_file_at_version(id: str, version: str) -> tuple:
    """Fetches file with given id at given version.

    Parameters:
        id: 12-character structure id
        version: version to fetch
    Returns:
        tuple of bytes and error code
    """

    category = id[1:3].lower()
    file_name = f"{id}_xyz_v{version}.cif.gz"
    url = f"{PDB_HTTP_FILE_URL}{category}/{id}/{file_name}"
    response = get(url)

    if response.status_code == 200:
        body = response.content
        return body, None
    return None, response.status_code
