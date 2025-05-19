"""Script for loading files for channel calculation from remote PDB database."""

import concurrent.futures as cf
import logging
import multiprocessing as mp
from gzip import GzipFile
from io import BytesIO
from queue import Full
from time import sleep

from requests import get

from app.channels.data.workers import create_inserter, create_managers
from app.config import PDB_SEARCH_API_LIMIT, WORKER_LIMIT
from app.log import log
from app.channels.data.utils import (
    create_output_directory,
    fetch_file,
    get_file_url,
    get_full_id,
    fetch_ids,
    get_last_version,
    get_search_url,
    create_queues,
)


def get_latest_versions(ids: list[str]) -> dict:
    """Returns dictionary of latest versions of each protein ID.

    Args:
        ids: List of strings.
    Returns:
        Dictionary with ids as keys and integers as values.
    """

    with cf.ThreadPoolExecutor(max_workers=WORKER_LIMIT) as executor:
        id_to_version = dict(zip(ids, executor.map(get_last_version, ids)))

    return id_to_version


def get_file_urls(ids: list[str], id_to_version: dict) -> dict[str, str]:
    """Returns url for fetching latest file for each protein ID.

    Args:
        ids: List of strings.
        id_to_version: Dict to get version for protein id.
    Returns:
        Dict of urls for given protein ids."""

    file_urls = {}
    for id in ids:
        version = id_to_version[id]
        file_urls[id] = get_file_url(id, version)

    return file_urls


def fetch_files(file_urls: dict, id_to_version: dict) -> tuple[list, list]:
    """Fetches files from given urls and returns SQLModel objects for insertion, also returns ids that failed.
    Args:
        file_urls: Dict of proteins and their urls.
        id_to_version: Dict to get version for protein id.
    Returns:
        List of files and list of failed ids."""

    with cf.ThreadPoolExecutor(max_workers=WORKER_LIMIT) as executor:
        id_to_data = dict(
            zip(file_urls.keys(), executor.map(fetch_file, file_urls.values()))
        )

    failed = []
    files = []

    for id, data in id_to_data.items():
        if data:
            full_id = get_full_id(id)
            version = id_to_version[id]
            data_io = BytesIO(data)
            with GzipFile(fileobj=data_io, mode="rb") as gz_file:
                cif_file = gz_file.read()
            files.append((full_id, version, cif_file))
        else:
            failed.append(id)

    return files, failed


# TODO check workers because it gets stuck after queue is full with no logs from workers -> no processing ?
def fetch_all(start: int, total: int, data_queue: mp.Queue) -> None:
    """Fetches IDs and corresponding latest file entries and stores them in database.

    Pushes files to data_queue for processing and waits if queue is full.
    Uses explicit timeouut to avoid overwhelming PDB APIs.

    Args:
        start: Starting id.
        total: Total number of ids to work with.
        data_queue: Queue for data processing.
    """
    log.debug("Entry fetching started.")

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    starts = [x for x in range(start, total, PDB_SEARCH_API_LIMIT)]
    log.debug(f"Created range starts: {starts}")

    total_processed = 0
    total_failed = 0

    for start in starts:
        url = get_search_url(start=start, limit=PDB_SEARCH_API_LIMIT)
        response = get(url)
        if response.status_code == 200 and "result_set" in (
            formatted := response.json()
        ):
            ids = [entry["identifier"] for entry in formatted["result_set"]]
            log.debug(f"Received {len(ids)} ids.")

            id_to_version = get_latest_versions(ids)
            file_urls = get_file_urls(ids, id_to_version)

            files_to_process, failed_batch = fetch_files(file_urls, id_to_version)

            while len(files_to_process) > 0:
                try:
                    file = files_to_process.pop(0)
                    data_queue.put(file)
                except Full:
                    files_to_process.insert(0, file)
                    log.debug("Data queue is full, waiting...")
                    sleep(2)

            total_processed += len(ids)
            total_failed += len(failed_batch)
            if failed_batch:
                log.debug(f"Number of failed ids: {len(failed_batch)}")
                with open("failed.txt", "a+") as file:
                    file.write("\n".join([x for x in failed_batch]))
        log.debug(
            f"Total processed: {total_processed} -- Total failed: {total_failed}."
        )

        # DO NOT DELETE!!!
        sleep(5)  # Required to avoid 'Too many requests' error
        # DO NOT DELETE!!!

    log.debug("Entry fetching finished.")

    logging.getLogger("requests").setLevel(logging.DEBUG)
    logging.getLogger("urllib3").setLevel(logging.DEBUG)


def run(start: int | None):
    """Creates and starts child processes for fetching file data.

    Args:
        start: Starting id for fetching.
    """
    log.info("Beggining fetch of all PDB entries.")
    response = fetch_ids(start=0, limit=0)

    create_output_directory()

    if response is not None:
        try:
            total = response["total_count"]
            log.debug(f"Total number of entries: {total}")
            actual_start = start if start else 0

            log.debug("Creating managers...")

            data_queue, result_queue = create_queues()

            managers = create_managers(data_queue=data_queue, result_queue=result_queue)
            inserter = create_inserter(result_queue=result_queue)

            log.debug("Workers created, starting main function...")
            fetch_all(start=actual_start, total=total, data_queue=data_queue)

            log.debug(
                "Tunnels calculations complete. Passing shutdown message to queues..."
            )
        finally:
            data_queue.put(None)
            result_queue.put(None)

            log.debug("Waiting for workers to stop.")
            for manager in managers:
                manager.join()

            inserter.join()
            log.info("Script finished.")
    else:
        log.error(f"Received unexpected status code: {response.status_code}")
