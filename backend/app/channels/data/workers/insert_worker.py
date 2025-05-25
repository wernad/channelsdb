"""Contains methods for creating and running inserter worker."""

import multiprocessing as mp
import time
from queue import Empty

from app.config import QUEUE_TIMEOUT
from app.log import log
from app.channels.data.workers.insert_utils import (
    insert_structure_if_missing,
    insert_channels,
    insert_profiles,
    insert_layers,
    insert_layer_residues,
    insert_het_residues,
)
from app.database.database import db_context


def insert_worker(result_queue: mp.Queue) -> None:
    """Worker process for inserting processed data by Mole workers.

    Transforms processed data into insert SQLModel models.
    Args:
        result_queue: Queue with results from other workers.
        timeout: How long to wait for queue.
    """
    log.debug("INSERTER -- Starting main process.")
    while True:
        try:
            data = result_queue.get(block=False)
            if data is None:
                log.debug("INSERTER -- Received shutdown message, stopping...")
                break

            full_id, version, method_id, channels = data
            log.debug(f"INSERTER -- Received data for: {full_id=}, {method_id=}")

            has_channels = True if channels else False
            with db_context() as session:
                try:
                    structure_id = insert_structure_if_missing(
                        session=session,
                        full_id=full_id,
                        version=version,
                        has_channels=has_channels,
                    )

                    if structure_id:
                        channels_ids = insert_channels(
                            session=session,
                            structure_id=structure_id,
                            method_id=method_id,
                            data=channels,
                        )

                        insert_profiles(
                            session=session, channels_ids=channels_ids, data=channels
                        )
                        layers_ids = insert_layers(
                            session=session, channels_ids=channels_ids, data=channels
                        )

                        insert_layer_residues(
                            session=session, layers_ids=layers_ids, data=channels
                        )
                        insert_het_residues(
                            session=session, channels_ids=channels_ids, data=channels
                        )
                        log.debug(
                            f"INSERTER -- Finished inserting channel data for: {full_id=}, {method_id=}"
                        )
                        session.commit()

                    else:
                        continue
                except Exception as e:
                    log.error(
                        f"INSERTER -- Expection occured during insertion, proceeding... Error: {e}"
                    )
        except Empty:
            log.debug("INSERTER -- Result queue is empty, waiting...")
            time.sleep(QUEUE_TIMEOUT)

    log.debug("INSERTER -- Successfully stopped.")


def create_inserter(result_queue: mp.Queue) -> mp.Process:
    """Creates a worker responsible for inserting processed data into database.

    Args:
        result_queue: Queue used by workers to push processed data into.
    Returns:
        Process instance.
    """

    log.debug("INSERTER -- Creating new inserter worker.")
    inserter = mp.Process(target=insert_worker, args=(result_queue,))
    inserter.start()
    log.debug("INSERTER -- Inserter worker created.")
    return inserter
