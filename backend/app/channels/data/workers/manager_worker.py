import multiprocessing as mp
import time
from queue import Empty

from app.config import MANAGER_LIMIT, QUEUE_TIMEOUT
from app.log import log
from app.channels.data.workers.command_worker import create_mole_workers


def worker_manager(
    manager_id: int, data_queue: mp.Queue, result_queue: mp.Queue
) -> None:
    """A worker responsible for creating Mole workers and inserting their outputs into database.

    Args:
        manager_id: Identifier of manager processes.
        data_queue: Queue for retrieving fetched files from main process.
        result_queue: Queue for sending data for insertion to inserter worker.
        queue_timeout: Time between queue checking.
    """

    workers = create_mole_workers(manager_id, data_queue, result_queue)
    shutdown = False
    log.debug(f"MANAGER {manager_id} -- Starting manager loop.")
    try:
        while not shutdown:
            try:
                log.debug(f"MANAGER {manager_id} -- Checking queue.")
                data = data_queue.get(block=False)

                if data is None:
                    log.debug(f"MANAGER {manager_id} -- Received shutdown signal.")
                    shutdown = True
                else:
                    log.debug(f"MANAGER {manager_id} -- Received new data to process.")
                    for _, worker_queue in workers:
                        worker_queue.put(data)
                    log.debug(f"MANAGER {manager_id} -- New data passed to workers.")
            except Empty:
                log.debug(f"MANAGER {manager_id} -- Data queue is empty, waiting.")
                time.sleep(QUEUE_TIMEOUT)
            except Exception as e:
                log.error(
                    f"MANAGER {manager_id} -- Unexpected error when reading data queue: {e}"
                )

    finally:
        log.debug(f"MANAGER {manager_id} -- Shutting down workers.")
        for worker, worker_queue in workers:
            worker_queue.put(None)

        for worker, _ in workers:
            worker.join()

        log.debug(f"MANAGER {manager_id} -- Workers shutdown successfully, exiting...")


def create_managers(data_queue: mp.Queue, result_queue: mp.Queue) -> list[mp.Process]:
    """Creates managers and main queue."""
    managers: list[mp.Process] = []

    for i in range(MANAGER_LIMIT):
        manager = mp.Process(target=worker_manager, args=(i, data_queue, result_queue))
        manager.name = f"M{i}"
        manager.start()
        managers.append(manager)

    return managers
