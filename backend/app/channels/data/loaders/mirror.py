import concurrent.futures as cf
import logging
import multiprocessing as mp
from gzip import GzipFile
from io import BytesIO
from queue import Full
from time import sleep


from app.channels.data.workers import create_inserter, create_managers
from app.config import MIRROR_API_LIMIT, WORKER_LIMIT
from app.log import log
from app.channels.data.utils import (
    create_output_directory,
    create_queues,
    fetch_file,
    fetch_total_count,
    get_file_url,
    fetch_ids,
)


def get_file_urls(ids: list[str]) -> list[str]:
    """Creates urls for given ids."""

    urls = {}

    for id in ids:
        urls[id] = get_file_url(id=id, remote=False)

    return urls


def fetch_files(file_urls: dict, id_to_version: dict) -> tuple[list, list]:
    """Fetches files from given urls and returns SQLModel objects for insertion, also returns ids that failed."""
    with cf.ThreadPoolExecutor(max_workers=WORKER_LIMIT) as executor:
        id_to_data = dict(
            zip(file_urls.keys(), executor.map(fetch_file, file_urls.values()))
        )

    failed = []
    files = []

    for id, data in id_to_data.items():
        if data:
            version = id_to_version[id]
            data_io = BytesIO(data)
            with GzipFile(fileobj=data_io, mode="rb") as gz_file:
                cif_file = gz_file.read()
            files.append((id, version, cif_file))
        else:
            failed.append(id)

    return files, failed


def fetch_all(start: int, total: int, data_queue: mp.Queue) -> None:
    """Fetches IDs and corresponding latest file entries and stores them in database.

    Pushes files to data_queue for processing and waits if queue is full.
    Uses explicit timeouut to avoid overwhelming PDB APIs.

    Args:
        start: starting id.
        total: total number of ids to work with.
        data_queue: Queue for data processing.
    """
    log.debug("Entry fetching started.")

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    starts = [x for x in range(start, total, MIRROR_API_LIMIT)]
    log.debug(f"Created range starts: {starts}")

    total_processed = 0
    total_failed = 0

    for start in starts:
        ids_with_versions = fetch_ids(
            start=start, limit=MIRROR_API_LIMIT, remote=False
        )["data"]
        print("@@@@", ids_with_versions)
        if ids_with_versions:
            ids = [entry["id"] for entry in ids_with_versions]
            log.debug(f"Received {len(ids_with_versions)} ids.")

            file_urls = get_file_urls(ids)

            print("panda")
            id_to_version = {
                entry["id"]: entry["version"] for entry in ids_with_versions
            }
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
        start: starting id for fetching.
    """
    log.info("Beggining fetch of all PDB entries.")
    total = fetch_total_count()

    create_output_directory()

    if total is not None:
        try:
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
