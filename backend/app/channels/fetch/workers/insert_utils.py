from app.log import log
from app.services import (
    ChannelService,
    HetResidueService,
    LayerResidueService,
    LayerService,
    ProfileService,
    StructureService,
    AnnotationService,
)

from app.database.database import db_context
from app.database.models import (
    RESIDUE_NAME_TO_ID,
    ChannelInsert,
    AnnotationInsert,
    HetResidueInsert,
    LayerInsert,
    LayerResidueInsert,
    ProfileInsert,
    Sources,
    StructureInsert,
)


def get_profile_values(
    channels_ids: list[int], data: list[list]
) -> list[ProfileInsert]:
    """Creates values for profile table insertion.

    Args:
        channels_ids: list of internal channel ids.
        data: channel data
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
                radius=round(float(profile_data["Radius"]), 3),
                free_radius=round(float(profile_data["FreeRadius"]), 3),
                t_value=round(float(profile_data["T"]), 3),
                distance=round(float(profile_data["Distance"]), 3),
                coord_x=round(float(profile_data["X"]), 3),
                coord_y=round(float(profile_data["Y"]), 3),
                coord_z=round(float(profile_data["Z"]), 3),
                charge=profile_data["Charge"],
            )
            values.append(entry)

    return values


def get_channel_values(
    structure_id: int, method_id: int, data: list[dict]
) -> list[ChannelInsert]:
    """Creates values list for inserting all channel entries.

    Args:
        structure_id: internal protein id
        data: list of channels as dicts.
    Returns:
        list of ChannelInsert objects.
    """
    log.debug(
        f"INSERTER -- Creating channel values for insert statement for structure: {structure_id}"
    )

    values = []

    for channel in data:
        entry = ChannelInsert(
            auto=channel["Auto"],
            cavity=channel["Cavity"],
            type=channel["Type"],
            structure_id=structure_id,
            method_id=method_id,
        )
        values.append(entry)

    return values


def get_annotation_values(
    channel_id: int, annotations: list[dict]
) -> list[AnnotationInsert]:
    """Creates values for insert for annotations for given channel and structure.

    Args:
        structure_id: internal protein id.
        channel_id: id of a channel.
        annotations: list of annotations in dict form.
    Returns:
        list of AnnotationInsert objects.
    """

    log.debug(
        f"INSERTER -- Creating annotation values for insert statement for channel {channel_id}"
    )
    values = []

    for ann in annotations:
        new_ann = AnnotationInsert(
            channel_id=channel_id,
            name=ann["Name"],
            description=ann["Description"],
            reference=ann["Reference"],
            reference_type=ann["ReferenceType"],
        )
        values.append(new_ann)

    log.debug(
        f"INSERTER -- Annotation values generated for structure channel {channel_id}"
    )
    return values


def get_layer_values(
    channels_ids: list[int], layers: list[dict]
) -> list[ChannelInsert]:
    """Creates values for insert for layer table per channel.

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
                radius=round(float(geometry["MinRadius"]), 3),
                free_radius=round(float(geometry["MinFreeRadius"]), 3),
                start_distance=round(float(geometry["StartDistance"]), 3),
                end_distance=round(float(geometry["EndDistance"]), 3),
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


def insert_structure_if_missing(
    full_id: str, version: int, has_channels: bool
) -> int | None:
    """Inserts a new structure row if it's not in the database.

    Args:
        full_id: full identifier of structure.
        version: Version of structure.
        has_channels: if protein has channels.
    Returns:
        integer id of structure entry or None if structure exists.
    """

    with db_context() as session:
        structure_service = StructureService(session)
        log.debug(f"INSERTER -- Checking if structure {full_id} exists.")
        structure = structure_service.check_if_exists_by_external_id(full_id)

        if structure is not None:
            return None

        else:
            new_structure = StructureInsert(
                has_channels=has_channels,
                version=version,
                external_id=full_id,
                source_id=Sources.PDB.value,
            )

            structure_id = structure_service.insert_entry(new_structure)

    log.debug(f"INSERTER -- Returning structure id: {structure_id}")
    return structure_id


def insert_profiles(channels_ids: list[int], data: list[dict]) -> None:
    """Inserts new profile entries for each new channel.

    Args:
        channels_ids: list of new internal channel ids.
        data: channel data.
    """

    log.debug(f"INSERTER -- Inserting profiles for channels: {channels_ids}")

    profiles = [channel["Profile"] for channel in data]

    values = get_profile_values(channels_ids=channels_ids, data=profiles)

    if values:
        with db_context() as session:
            profile_service = ProfileService(session)

            profile_service.insert_bulk(values)

        log.debug(f"INSERTER -- Profiles inserted for channels: {channels_ids}")
    else:
        log.debug(f"INSERTER -- No profile values for channels: {channels_ids}")


def insert_channels(structure_id: int, method_id: int, data: dict) -> list[int] | None:
    """Inserts new channels into database.

    If protein entry doesn't exist, insert it as well.

    Args:
        structure_id: internal id of protein entry.
        method_id: method used to calculate channels.
        data: channels data from command worker.
    Returns:
        list of newly added ids.
    """

    log.debug(
        f"INSERTER -- Inserting channels for: structure {structure_id}, method: {method_id}"
    )

    values = get_channel_values(structure_id, method_id, data)
    if values:
        with db_context() as session:
            channel_service = ChannelService(session)

            channels_ids = channel_service.insert_in_bulk(values)

        log.debug(
            f"INSERTER -- Channels inserted for: structure {structure_id}, method: {method_id}"
        )
        return channels_ids

    log.debug(
        f"INSERTER -- No channel values for: structure {structure_id}, method: {method_id}"
    )
    return None


def insert_annotations(channel_id: int, annotation_data: dict) -> None:
    """Inserts annotation data for given channel.

    Args:
        channel_id: internal id of channel.
        annotation_data: dict with annotation data.
    """

    log.debug(f"INSERTER -- Inserting annotations for channel: {channel_id}")

    values = get_annotation_values(annotation_data)

    if values:
        with db_context() as session:
            annotation_service = AnnotationService(session)

            annotation_service.insert_bulk(values)

        log.debug(f"INSERTER -- Annotations isnerted for channel: {channel_id}")
    else:
        log.debug(f"INSERTER -- No annotation values for channel: {channel_id}")


def insert_layers(channels_ids: list[int], data: list[dict]) -> list[int] | None:
    """Inserts new layers for new channels.

    Args:
        channels_ids: list of new internal channel ids.
        data: channel data.
    Returns:
        list of newly added layers per channel.
    """
    log.debug(f"INSERTER -- Inserting layers for these channels: {channels_ids}")

    layers = [channel["Layers"]["LayersInfo"] for channel in data]

    values = get_layer_values(channels_ids, layers)

    if values:
        with db_context() as session:
            layers_service = LayerService(session)

            layers_ids = layers_service.insert_bulk(values)

        log.debug(f"INSERTER -- Layers inserted for channels: {channels_ids}")
        return layers_ids

    log.debug(f"INSERTER -- No layer values for channels: {channels_ids}")
    return None


def insert_layer_residues(layers_ids: list[int], data: list[dict]) -> None:
    """Inserts new layer residue entries for each layer.

    Args:
        layers_ids: list of internal layer ids.
        data: channel data.
    """

    log.debug(f"INSERTER -- Inserting layer residues for these layers: {layers_ids}")

    layer_residues = [
        layer["Residues"]
        for channel in data
        for layer in channel["Layers"]["LayersInfo"]
    ]

    values = get_layer_residue_values(
        layers_ids=layers_ids, layer_residues=layer_residues
    )

    if values:
        with db_context() as session:
            layer_residue_service = LayerResidueService(session)

            layer_residue_service.insert_bulk(values)

        log.debug(f"INSERTER -- Layer residues inserted for layers: {layers_ids}")
    else:
        log.debug(f"INSERTER -- No layer residue values for layers: {layers_ids}")


def insert_het_residues(channels_ids: list[int], data: list[dict]) -> None:
    """Inserts new het residue entries for each layer.

    Args:
        channels_ids: list of internal channel ids.
        data: channel data.
    """

    log.debug(f"INSERTER -- Inserting het residues for these channels: {channels_ids}")
    het_residues = [channel["Layers"]["HetResidues"] for channel in data]

    values = get_het_residue_values(
        channels_ids=channels_ids, het_residues=het_residues
    )
    if values:
        with db_context() as session:
            het_residue_service = HetResidueService(session)

            het_residue_service.insert_bulk(values)

        log.debug(f"INSERTER -- Het residues inserted for channels: {channels_ids}")
    else:
        log.debug(f"INSERTER -- No Het residue values for channels: {channels_ids}")
