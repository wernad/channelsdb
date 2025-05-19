from enum import StrEnum
from queue import Full
from time import sleep
from zoneinfo import ZoneInfo
import multiprocessing as mp
from os import environ

from apscheduler.events import (
    EVENT_JOB_ERROR,
    EVENT_JOB_EXECUTED,
    EVENT_JOB_MISSED,
    SchedulerEvent,
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from arrow import utcnow
from requests import get

from app.config import CRON_JOB_DAY, MIRROR_API_PATH
from app.database.database import db_context
from app.log import log
from app.channels.data.utils import create_output_directory, create_queues
from app.channels.data.loaders.mirror import fetch_files, get_file_urls
from app.services import StructureService
from app.channels.data.workers import create_inserter, create_managers

__all__ = ["get_scheduler"]


class Action(StrEnum):
    ADDED = "added"
    MODIFIED = "modified"
    OBSOLETE = "obsolete"


def get_changes(from_date: str, change_type: Action) -> list[str]:
    """Fetches changes of new, updated or removed entries."""
    log.debug(f"Trying to fetch changes for '{change_type.value}' entries.")
    api = environ.get("MIRROR_API_URL", MIRROR_API_PATH)
    url = f"{api}proteins/changes/{change_type.value}/{from_date}"
    response = get(url)

    if response.status_code == 200:
        log.debug("Data sucessfully fetched.")
        return response.json()

    log.error(f"No changes found for '{change_type.value}' entries.")
    return []


def get_last_date():
    """Gets last date when files were updated (currently Friday)."""
    today = utcnow()
    last_date = today.shift(weeks=-1, weekday=5).format("YYYYMMDD")
    return last_date


def send_to_process(data_queue: mp.Queue, files_to_process: list[tuple]) -> int:
    log.debug("SCHEDULER - Sending filesto data queue")
    while len(files_to_process) > 0:
        try:
            file = files_to_process.pop(0)
            data_queue.put(file)
        except Full:
            files_to_process.insert(0, file)
            log.debug("SCHEDULER - Data queue is full, waiting...")
            sleep(2)


def process_valid():
    """Processes added or updated entries based on flag."""
    log.debug("Processing added and modified entries.")
    last_date = get_last_date()

    added = get_changes(last_date, Action.ADDED)
    modified = get_changes(last_date, Action.MODIFIED)

    try:
        create_output_directory()
        data_queue, result_queue = create_queues()

        log.debug("SCHEDULER - Creating managers...")
        managers = create_managers(data_queue=data_queue, result_queue=result_queue)
        inserter = create_inserter(result_queue=result_queue)
        log.debug("SCHEDULER - Managers created.")

        # Added
        log.debug("SCHEDULER - Processing 'added' entries.")
        ids_added = [entry["id"] for entry in added]
        file_urls = get_file_urls(ids_added)
        id_to_version_added = {id: 1 for id in ids_added}
        files_to_process, failed_batch = fetch_files(file_urls, id_to_version_added, 5)

        send_to_process(data_queue=data_queue, files_to_process=files_to_process)

        if added:
            log.debug("SCHEDULER - Finished processing 'added' entries.")

        total_failed = len(failed_batch)
        total_processed = len(added)

        log.debug(
            f"SCHEDULER - Finished processing 'added' files: {total_processed=}, {total_failed=}"
        )

        # Modified
        log.debug("SCHEDULER - Processing 'modified' entries.")
        ids_modified = [entry["id"] for entry in modified]
        file_urls = get_file_urls(ids_modified)
        id_to_version_modified = {entry["id"]: entry["version"] for entry in modified}
        files_to_process, failed_batch = fetch_files(file_urls, id_to_version_modified)

        send_to_process(data_queue=data_queue, files_to_process=files_to_process)

        if modified:
            log.debug("SCHEDULER - Finished processing 'modified' entries.")

        total_processed = len(modified)
        total_failed = len(failed_batch)

        log.debug(
            f"SCHEDULER - Finished processing modified files: {total_processed=}, {total_failed=}"
        )
    except Exception as e:
        log.error(f"SCHEDULER - An unexpected error occured: {e}")
    finally:
        log.debug("SCHEDULER - Shutting down managers.")
        for _ in managers:
            data_queue.put(None)
            data_queue.put(None)  # Intended doubling of 'shutdown' messages.

        result_queue.put(None)

        log.debug("SCHEDULER - Waiting for managers to stop.")
        for manager in managers:
            manager.join()

        log.debug("SCHEDULER - Waiting for inserter to stop.")
        inserter.join()
        log.info("Script finished.")

        log.info("SCHEDULER - Added/Modified entry processing finished.")


def process_obsolete() -> None:
    """Handles processing of removed entries."""
    log.debug("Processing obsolete entries.")
    last_date = get_last_date()
    with db_context() as session:
        structure_service = StructureService(session)
        log.debug("SCHEDULER - Start processing 'obsolete' entries.")

        obsolete = get_changes(last_date, Action.OBSOLETE)
        failed = []

        for id in obsolete:
            _ = structure_service.delete_structure_by_external_id(protein_id=id)

        if obsolete:
            log.debug(
                f"SCHEDULER - Finished processing obsolete entries with {len(failed)} failures."
            )


def event_listener(event: SchedulerEvent):
    """Event handler for checking event status."""
    if event.code == EVENT_JOB_ERROR:
        log.error(
            f"Fetching job crashed because of: {event.exception}\n{event.traceback}"
        )
    elif event.code == EVENT_JOB_EXECUTED:
        log.info("Fetching job was sucessfuly completed.")
    elif event.code == EVENT_JOB_MISSED:
        log.debug(
            "Fetching job missed it's planned execution. It will be re-executed at next available time."
        )


def get_scheduler():
    """Creates and configures a new scheduler and returns in."""
    log.debug(f"SCHEDULER - Creating background tasks with day of week {CRON_JOB_DAY}.")
    scheduler = BackgroundScheduler()

    CET = ZoneInfo("Europe/Prague")
    trigger = CronTrigger(day_of_week=CRON_JOB_DAY, hour=0, minute=0, timezone=CET)

    scheduler.add_job(
        func=process_valid,
        trigger=trigger,
        replace_existing=True,
        id="fetch_added_and_modified",
        coalesce=True,
        max_instances=1,
    )

    scheduler.add_job(
        func=process_obsolete,
        trigger=trigger,
        replace_existing=True,
        id="fetch_obsolete",
        coalesce=True,
        max_instances=1,
    )
    scheduler.add_listener(
        event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_MISSED | EVENT_JOB_ERROR
    )

    log.debug("SCHEDULER - Background task created.")
    return scheduler
