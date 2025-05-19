"""Script for loading JSON data from previous version of ChannelsDB into database."""

import json
import sys
from pathlib import Path

from app.database.models import METHODS_NAMES_TO_IDS
from app.channels.data.utils import get_full_id

from app.channels.data.workers.insert_utils import (
    insert_structure_if_missing,
    insert_channels,
    insert_annotations,
    insert_profiles,
    insert_layers,
    insert_layer_residues,
    insert_het_residues,
)


def load_json_file(file_path) -> dict:
    """
    Load and parse a JSON file from the specified path.

    Args:
        file_path: Path to the JSON file

    Returns:
        dict: The parsed JSON data
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading file: {e}")
        sys.exit(1)


def get_annotations_ids(annotations: list[dict]) -> dict:
    """Extracts ids of annotatated channels and correspoding annotations' ids.

    Args:
        annotations: list of annotations.
    Returns:
        dictionary of channel ids as key and indices of annotations as values.
    """

    result = {}

    for idx, ann in enumerate(annotations):
        id = ann["Id"]
        if id not in result:
            result[id] = [idx]
        else:
            result[id].append(idx)

    return result


def run(file_path: str) -> None:
    """Loads JSON file from given path and starts loading channels into database.

    Args:
        file_path: path to JSON file.
    """

    external_id = Path(file_path).name.split(".")[0]
    full_id = get_full_id(external_id)

    json_file = load_json_file(file_path)

    annotations_indices = get_annotations_ids(json_file["Annotations"])
    structure_id = insert_structure_if_missing(
        full_id=full_id, version=1, has_channels=True
    )

    for method, channels in json_file["Channels"].items():
        if channels:
            method_id = METHODS_NAMES_TO_IDS[method]

            channels_ids = insert_channels(
                structure_id=structure_id, method_id=method_id, data=channels
            )

            for channel_idx, channel in enumerate(channels):
                ann_indices = annotations_indices.get(channel["Id"], None)

                if ann_indices:
                    selected_annotations = []
                    for idx in ann_indices:
                        selected_annotations.append(json_file["Annotations"][idx])

                    insert_annotations(
                        channel_id=channel_idx, annotation_data=selected_annotations
                    )

            insert_profiles(channels_ids=channels_ids, data=channels)
            layers_ids = insert_layers(channels_ids=channels_ids, data=channels)

            insert_layer_residues(layers_ids=layers_ids, data=channels)
            insert_het_residues(channels_ids=channels_ids, data=channels)
