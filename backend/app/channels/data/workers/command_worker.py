import multiprocessing as mp
import os
import shutil
import time
from queue import Empty

from defusedxml import ElementTree

from app.config import CONFIG_PATH, OUTPUT_PATH, QUEUE_TIMEOUT
from app.log import log
from app.channels.commands import MoleCofactor, MoleCognate, MoleCSA
from app.channels.data.types import MoleClass


def _load_config_file(file_name: str) -> ElementTree:
    """Loads xml configuration file, parses it and returns it.

    Returns:
        Parsed XML ElementTree.
    """
    file_path = f"{CONFIG_PATH}/{file_name}.xml"
    with open(file_path) as file:
        parsed = ElementTree.parse(file)

    return parsed


def _prepare_work_dir(worker_id: str) -> None:
    """Creates a new folder and updates working directory for given worker.

    Args:
        worker_id: id of worker.
    """

    work_dir = f"{OUTPUT_PATH}/{worker_id}"

    try:
        os.mkdir(f"{work_dir}")
        os.chdir(work_dir)
        log.debug("Working directory created and set successfully.")
    except FileExistsError:
        log.error(f"Directory '{work_dir}' already exists.")
    except PermissionError:
        log.error(f"Permission denied: Unable to create '{work_dir}'.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")


def _cleanup() -> None:
    """Deletes everything in the current working directory."""
    for item in os.listdir():
        if os.path.isfile(item) or os.path.islink(item):
            os.unlink(item)
        elif os.path.isdir(item):
            shutil.rmtree(item)


def command_worker(
    worker_id: int,
    manager_id: int,
    mole_class: MoleClass,
    data_queue: mp.Queue,
    result_queue: mp.Queue,
) -> None:
    """A worker method that runs Mole software and extracted tunnel data.

    If cognate command object raises KeyError, skips calculation.

    Args:
        worker_id: Identifier for this worker.
        manager_id: Identifier of manager process.
        mole_class: subclass to use for Mole execution.
        data_queue: Queue to retrieve tasks from.
        result_queue: used to send results back to manager.
    """
    worker_id = f"M{manager_id}_W{worker_id}"
    config_file = _load_config_file(mole_class.TUNNEL_TYPE)
    _prepare_work_dir(worker_id)

    log.debug(
        f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Starting worker."
    )

    command: MoleClass = mole_class(worker_id, config_file)
    try:
        while True:
            try:
                log.debug(
                    f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Waiting for data."
                )
                data = data_queue.get(block=False, timeout=QUEUE_TIMEOUT)

                if not data:
                    log.debug(
                        f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Empty message received, terminating worker."
                    )
                    break

                log.debug(
                    f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Data received, processing..."
                )
                full_id, version, file = data
                command.create_source_file(full_id, file)
                try:
                    command.configure(full_id)
                except KeyError:
                    log.error(
                        f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} {mole_class.TUNNEL_TYPE.upper()} -- Canceling cognate calculation for protein {full_id}"
                    )
                    command.cleanup()
                    continue

                command.execute(full_id)

                result = command.retrieve()

                if result:
                    log.debug(
                        f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Data processed, sending results to inserter."
                    )

                    queue_entry = (full_id, version, command.METHOD_ID, result)
                    result_queue.put(queue_entry)
                else:
                    log.debug(
                        f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Data processed, sending results to inserter."
                    )

                command.cleanup()
            except Empty:
                log.debug(
                    f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Queue empty, waiting."
                )
                time.sleep(QUEUE_TIMEOUT)
    finally:
        _cleanup()
        log.debug(
            f"WORKER {worker_id} {mole_class.TUNNEL_TYPE.upper()} -- Final clean up complete."
        )


def create_mole_workers(
    manager_id: int, data_queue: mp.Queue, result_queue: mp.Queue
) -> list[mp.Process]:
    """Creates a set of Mole workers for each Mole method.

    Args:
        manager_id: Identifier of manager process.
        mole_class: subclass to use for Mole execution.
        data_queue: Queue to retrieve tasks from.
        result_queue: used to send results back to manager.
    """

    log.debug(f"MANAGER {manager_id} -- Creating workers.")
    classes = [MoleCofactor, MoleCognate, MoleCSA]

    workers: list[tuple[mp.Process, mp.Queue]] = []

    for idx, mole_class in enumerate(classes):
        new_worker = mp.Process(
            target=command_worker,
            args=(idx, manager_id, mole_class, data_queue, result_queue),
        )
        new_worker.daemon = True
        new_worker.name = f"M{manager_id}_W{idx}"
        new_worker.start()
        workers.append((new_worker, data_queue))

    log.debug(f"MANAGER {manager_id} -- Workers created.")
    return workers
