import multiprocessing as mp
import time
from queue import Empty

from app.config import QUEUE_TIMEOUT
from app.database.database import db_context
from app.database.models import (CATEGORIES_NAME_TO_ID, RESIDUE_NAME_TO_ID,
                                 ChannelInsert, HetResidueInsert, LayerInsert,
                                 LayerResidueInsert, ProfileInsert, Sources,
                                 StructureInsert)
from app.log import log
from app.services import (ChannelService, HetResidueService,
                          LayerResidueService, LayerService, ProfileService,
                          StructureService)


def insert_structure_if_missing(full_id: str, version: int) -> int:
    """Inserts a new structure row if it's not in the database.

    Args:
        full_id: full identifier of structure.
        version: Version of structure.
    Returns:
        integer id of structure entry.
    """

    with db_context() as session:
        structure_service = StructureService(session)
        log.debug(f"INSERTER -- Checking if structure {full_id} exists.")
        structure_id = structure_service.check_if_exists_by_external_id(full_id)
        if structure_id is None:
            new_structure = StructureInsert(
                has_channels=False,
                version=version,
                external_id=full_id,
                source_id=Sources.PDB.value,
            )

            structure_id = structure_service.insert_entry(new_structure)
    log.debug(f"INSERTER -- Returning structure id: {structure_id}")
    return structure_id


def get_profile_values(
    channels_ids: list[int], data: list[list]
) -> list[ProfileInsert]:
    """Creates values for profile table insertion.

    Args:
        channels_ids: list of internal channel ids.
        data: tunnel data
    Returns:
        list of ProfileInsert objects.
    """
    log.debug(
        f"INSERTER -- Creating channel values for insert statement for channels: {channels_ids}"
    )

    values = []
    for channel_id, profiles in zip(channels_ids, data):
        for profile_data in profiles:
            entry = ProfileInsert(
                channel_id=channel_id,
                radius=round(profile_data["Radius"], 3),
                free_radius=round(profile_data["FreeRadius"], 3),
                t_value=round(profile_data["T"], 3),
                distance=round(profile_data["Distance"], 3),
                coord_x=round(profile_data["X"], 3),
                coord_y=round(profile_data["Y"], 3),
                coord_z=round(profile_data["Z"], 3),
                charge=profile_data["Charge"],
            )
            values.append(entry)

    return values


def get_channel_values(
    structure_id: int, method_id: int, data: list[dict]
) -> list[ChannelInsert]:
    """Creates values list for inserting all tunnel entries.

    Args:
        structure_id: internal protein id
        data: list of tunnels as dicts.
    Returns:
        list of ChannelInsert objects.
    """
    log.debug(
        f"INSERTER -- Creating channel values for insert statement for structure: {structure_id}"
    )

    values = []

    for tunnel in data:
        type_ = tunnel["Type"]
        category_id = CATEGORIES_NAME_TO_ID[type_]
        entry = ChannelInsert(
            auto=tunnel["Auto"],
            cavity=tunnel["Cavity"],
            structure_id=structure_id,
            method_id=method_id,
            category_id=category_id,
        )
        values.append(entry)

    return values


def get_layer_values(
    channels_ids: list[int], layers: list[dict]
) -> list[ChannelInsert]:
    """Inserts new layer entries for each new channel.

    Args:
        channels_ids: list of new internal channel ids.
        layers: layer data.
    Returns:
        list of ChannelInsert object.
    """
    log.debug(
        f"INSERTER -- Creating layers values for insert statement for channels: {channels_ids}"
    )
    values = []

    for idx, (channel_id, layer) in enumerate(zip(channels_ids, layers)):
        for layer_data in layer:
            geometry = layer_data["LayerGeometry"]
            bottleneck = geometry.get("Bottleneck", False)
            new_layer = LayerInsert(
                channel_id=channel_id,
                radius=round(geometry["MinRadius"], 3),
                free_radius=round(geometry["MinFreeRadius"], 3),
                start_distance=round(geometry["StartDistance"], 3),
                end_distance=round(geometry["EndDistance"], 3),
                local_minimum=geometry["LocalMinimum"],
                bottleneck=bottleneck,
                layer_order=idx + 1,
            )

            values.append(new_layer)

    log.debug(f"INSERTER -- Layer values generated for channels: {channels_ids}")
    return values


def get_layer_residue_values(
    layers_ids: list[int], layer_residues: list[list]
) -> list[LayerResidueInsert]:
    """Generates values for layer residue values of given layers.

    Args:
        layers_ids: internal ids of new layers.
        layer_residues: list of residues in a layer.
    Returns:
        list of LayerResidueInsert object.
    """

    log.debug(
        f"INSERTER -- Creating layer residues values for insert statement for layers: {layers_ids}"
    )

    values = []

    for layer_id, layer_residue in zip(layers_ids, layer_residues):
        for idx, residue_data in enumerate(layer_residue):
            split_data = residue_data.split(" ")
            if len(split_data) == 3:
                residue, seq, chain = split_data
                backbone = False
            else:
                residue, seq, chain = split_data[:3]
                backbone = True
            new_layer_residue = LayerResidueInsert(
                layer_id=layer_id,
                sequence_number=seq,
                backbone=backbone,
                chain_id=chain,
                flow_id=idx,
                residue_id=RESIDUE_NAME_TO_ID.get(residue, None),
            )

            values.append(new_layer_residue)

    log.debug(f"INSERTER -- Layer residue values generated for layers: {layers_ids}")
    return values


def get_het_residue_values(
    channels_ids: list[int], het_residues: list[list]
) -> list[HetResidueInsert]:
    """Generates values for het residue values of given channels.

    Args:
        channels_ids: list of internal ids for channels.
        het_residues: list of het residues in a layer.
    Returns:
        list of HetResidueInsert object.
    """

    log.debug(
        f"INSERTER -- Creating het residue values for insert statement for channels: {channels_ids}"
    )
    values = []

    for channel_id, het_residue in zip(channels_ids, het_residues):
        for residue_data in het_residue:
            split_data = residue_data.split(" ")
            if len(split_data) == 3:
                residue, seq, chain = split_data
                backbone = False
            else:
                residue, seq, chain = split_data[:3]
                backbone = True
            new_layer_residue = HetResidueInsert(
                channel_id=channel_id,
                sequence_number=seq,
                backbone=backbone,
                chain_id=chain,
                residue_id=RESIDUE_NAME_TO_ID.get(residue, None),
            )

            values.append(new_layer_residue)

    log.debug(f"INSERTER -- Het residue values generated for channels: {channels_ids}")
    return values


def insert_profiles(channels_ids: list[int], data: list[dict]) -> None:
    """Inserts new profile entries for each new channel.

    Args:
        channels_ids: list of new internal channel ids.
        data: tunnel data.
    """

    log.debug(f"INSERTER -- Inserting profiles for channels: {channels_ids}")

    profiles = [tunnel["Profile"] for tunnel in data]

    values = get_profile_values(channels_ids=channels_ids, data=profiles)

    with db_context() as session:
        profile_service = ProfileService(session)

        profile_service.insert_bulk(values)

    log.debug(f"INSERTER -- Profiles inserted for channels: {channels_ids}")


def insert_channels(structure_id: int, method_id: int, data: dict) -> list[int]:
    """Inserts new tunnels into database.

    If protein entry doesn't exist, insert it as well.

    Args:
        structure_id: internal id of protein entry.
        method_id: method used to calculate tunnels.
        data: tunnels data from command worker.
    Returns:
        list of newly added ids.
    """

    log.debug(
        f"INSERTER -- Inserting channels for: structure {structure_id}, method: {method_id}"
    )

    values = get_channel_values(structure_id, method_id, data)

    with db_context() as session:
        channel_service = ChannelService(session)

        channels_ids = channel_service.insert_in_bulk(values)

    log.debug(
        f"INSERTER -- Channels inserted for: structure {structure_id}, method: {method_id}"
    )
    return channels_ids


def insert_layers(channels_ids: list[int], data: list[dict]) -> list[int]:
    """Inserts new layers for new channels.

    Args:
        channels_ids: list of new internal channel ids.
        data: tunnel data.
    Returns:
        list of newly added layers per channel.
    """
    log.debug(f"INSERTER -- Inserting layers for these channels: {channels_ids}")

    layers = [tunnel["Layers"]["LayersInfo"] for tunnel in data]

    values = get_layer_values(channels_ids, layers)

    with db_context() as session:
        layers_service = LayerService(session)

        layers_ids = layers_service.insert_bulk(values)

    log.debug(f"INSERTER -- layers inserted for channels: {channels_ids}")
    return layers_ids


def insert_layer_residues(layers_ids: list[int], data: list[dict]) -> None:
    """Inserts new layer residue entries for each layer.

    Args:
        layers_ids: list of internal layer ids.
        data: tunnel data.
    """

    log.debug(f"INSERTER -- Inserting residues for these layers: {layers_ids}")

    layer_residues = [
        layer["Residues"] for tunnel in data for layer in tunnel["Layers"]["LayersInfo"]
    ]

    values = get_layer_residue_values(
        layers_ids=layers_ids, layer_residues=layer_residues
    )

    with db_context() as session:
        layer_residue_service = LayerResidueService(session)

        layer_residue_service.insert_bulk(values)

    log.debug(f"INSERTER -- Residues inserted for layers: {layers_ids}")


def insert_het_residues(channels_ids: list[int], data: list[dict]) -> None:
    """Inserts new het residue entries for each layer.

    Args:
        channels_ids: list of internal channel ids.
        data: tunnel data.
    """

    log.debug(f"INSERTER -- Inserting het residues for these channels: {channels_ids}")
    het_residues = [tunnel["Layers"]["HetResidues"] for tunnel in data]

    values = get_het_residue_values(
        channels_ids=channels_ids, het_residues=het_residues
    )

    with db_context() as session:
        het_residue_service = HetResidueService(session)

        het_residue_service.insert_bulk(values)

    log.debug(f"INSERTER -- Het residues inserted for channels: {channels_ids}")


def insert_worker(result_queue: mp.Queue) -> None:
    """Worker process for inserting processed data by Mole workers.

    Transforms processed data into insert SQLModel models.
    Args:
        result_queue: queue with results from other workers.
        timeout: how long to wait for queue.
    """
    log.debug("INSERTER -- Starting main process.")
    while True:
        try:
            data = result_queue.get(block=False)
            if data is None:
                log.debug("INSERTER -- Received shutdown message, stopping...")
                break

            full_id, version, method_id, tunnels = data
            log.debug(f"INSERTER -- Received data for: {full_id=}, {method_id=}")

            structure_id = insert_structure_if_missing(full_id=full_id, version=version)

            channels_ids = insert_channels(
                structure_id=structure_id, method_id=method_id, data=tunnels
            )

            insert_profiles(channels_ids=channels_ids, data=tunnels)
            layers_ids = insert_layers(channels_ids=channels_ids, data=tunnels)

            insert_layer_residues(layers_ids=layers_ids, data=tunnels)
            insert_het_residues(channels_ids=channels_ids, data=tunnels)
            log.debug(
                f"INSERTER -- Finished inserting channel data for: {full_id=}, {method_id=}"
            )
        except Empty:
            log.debug("INSERTER -- Result queue is empty, waiting...")
            time.sleep(QUEUE_TIMEOUT)

    log.debug("INSERTER -- Successfully stopped.")


def create_inserter(result_queue: mp.Queue) -> mp.Process:
    """Creates a worker responsible for inserting processed data into database.

    Args:
        result_queue: queue used by workers to push processed data into.
    Returns:
        Process instance.
    """

    log.debug("INSERTER -- Creating new inserter worker.")
    inserter = mp.Process(target=insert_worker, args=(result_queue,))
    inserter.start()
    log.debug("INSERTER -- Inserter worker created.")
    return inserter
