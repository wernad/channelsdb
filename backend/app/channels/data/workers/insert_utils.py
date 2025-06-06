"""Methods for inserting values used by inserter worker."""

from sqlmodel import Session
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
        channels_ids: List of internal channel ids.
        data: Channel data
    Returns:
        List of ProfileInsert objects.
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
        structure_id: Internal protein id
        data: List of channels as dicts.
    Returns:
        List of ChannelInsert objects.
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
        structure_id: Internal protein id.
        channel_id: Id of a channel.
        annotations: List of annotations in dict form.
    Returns:
        List of AnnotationInsert objects.
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
        channels_ids: List of new internal channel ids.
        layers: Layer data.
    Returns:
        List of ChannelInsert object.
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
        layers_ids: Internal ids of new layers.
        layer_residues: List of residues in a layer.
    Returns:
        List of LayerResidueInsert object.
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
        channels_ids: List of internal ids for channels.
        het_residues: List of het residues in a layer.
    Returns:
        List of HetResidueInsert object.
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
    session: Session,
    full_id: str,
    version: int,
    has_channels: bool,
    skip_existing: bool,
    is_pdb: bool = True,
) -> int | None:
    """Inserts a new structure row if it's not in the database.

    Args:
        full_id: Full identifier of structure.
        version: Version of structure.
        has_channels: If protein has channels.
        skip_existing: If already present structures should be returned or skipped.
        is_pdb: type of id.
    Returns:
        Integer id of structure entry or None if structure exists.
    """

    structure_service = StructureService(session)
    log.debug(f"INSERTER -- Checking if structure {full_id} exists.")
    structure = structure_service.check_if_exists_by_external_id_and_version(
        full_id, version
    )

    if structure is not None:
        log.debug(
            f"Structure {full_id} at version {version} already exists. Skip: {skip_existing}"
        )
        return None if skip_existing else structure.id

    else:
        new_structure = StructureInsert(
            has_channels=has_channels,
            version=version,
            external_id=full_id,
            source_id=Sources.PDB.value if is_pdb else Sources.ALPHAFILL.value,
        )

        structure_id = structure_service.insert_entry(new_structure)

    log.debug(f"INSERTER -- Returning structure id: {structure_id}")
    return structure_id


def insert_profiles(
    session: Session, channels_ids: list[int], data: list[dict]
) -> None:
    """Inserts new profile entries for each new channel.

    Args:
        channels_ids: List of new internal channel ids.
        data: Channel data.
    """

    log.debug(f"INSERTER -- Inserting profiles for channels: {channels_ids}")

    profiles = [channel["Profile"] for channel in data]

    values = get_profile_values(channels_ids=channels_ids, data=profiles)

    if values:
        profile_service = ProfileService(session)

        profile_service.insert_bulk(values)

        log.debug(f"INSERTER -- Profiles inserted for channels: {channels_ids}")
    else:
        log.debug(f"INSERTER -- No profile values for channels: {channels_ids}")


def insert_channels(
    session: Session, structure_id: int, method_id: int, data: dict
) -> list[int] | None:
    """Inserts new channels into database.

    If protein entry doesn't exist, insert it as well.

    Args:
        structure_id: Internal id of protein entry.
        method_id: Method used to calculate channels.
        data: Channels data from command worker.
    Returns:
        List of newly added ids.
    """

    log.debug(
        f"INSERTER -- Inserting channels for: structure {structure_id}, method: {method_id}"
    )

    values = get_channel_values(structure_id, method_id, data)
    if values:
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


def insert_annotations(
    session: Session, channel_id: int, annotation_data: dict
) -> None:
    """Inserts annotation data for given channel.

    Args:
        channel_id: Internal id of channel.
        annotation_data: Dict with annotation data.
    """

    log.debug(f"INSERTER -- Inserting annotations for channel: {channel_id}")

    values = get_annotation_values(channel_id, annotation_data)

    if values:
        annotation_service = AnnotationService(session)

        annotation_service.insert_bulk(values)

        log.debug(f"INSERTER -- Annotations isnerted for channel: {channel_id}")
    else:
        log.debug(f"INSERTER -- No annotation values for channel: {channel_id}")


def insert_layers(
    session: Session, channels_ids: list[int], data: list[dict]
) -> list[int] | None:
    """Inserts new layers for new channels.

    Args:
        channels_ids: List of new internal channel ids.
        data: Channel data.
    Returns:
        List of newly added layers per channel.
    """
    log.debug(f"INSERTER -- Inserting layers for these channels: {channels_ids}")

    layers = [channel["Layers"]["LayersInfo"] for channel in data]

    values = get_layer_values(channels_ids, layers)

    if values:
        layers_service = LayerService(session)

        layers_ids = layers_service.insert_bulk(values)

        log.debug(f"INSERTER -- Layers inserted for channels: {channels_ids}")
        return layers_ids

    log.debug(f"INSERTER -- No layer values for channels: {channels_ids}")
    return None


def insert_layer_residues(
    session: Session, layers_ids: list[int], data: list[dict]
) -> None:
    """Inserts new layer residue entries for each layer.

    Args:
        layers_ids: List of internal layer ids.
        data: Channel data.
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
        layer_residue_service = LayerResidueService(session)

        layer_residue_service.insert_bulk(values)

        log.debug(f"INSERTER -- Layer residues inserted for layers: {layers_ids}")
    else:
        log.debug(f"INSERTER -- No layer residue values for layers: {layers_ids}")


def insert_het_residues(
    session: Session, channels_ids: list[int], data: list[dict]
) -> None:
    """Inserts new het residue entries for each layer.

    Args:
        channels_ids: List of internal channel ids.
        data: Channel data.
    """

    log.debug(f"INSERTER -- Inserting het residues for these channels: {channels_ids}")
    het_residues = [channel["Layers"]["HetResidues"] for channel in data]

    values = get_het_residue_values(
        channels_ids=channels_ids, het_residues=het_residues
    )
    if values:
        het_residue_service = HetResidueService(session)

        het_residue_service.insert_bulk(values)

        log.debug(f"INSERTER -- Het residues inserted for channels: {channels_ids}")
    else:
        log.debug(f"INSERTER -- No Het residue values for channels: {channels_ids}")
