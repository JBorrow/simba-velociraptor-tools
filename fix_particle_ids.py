"""
This script "fixes up" the particle IDs; it's the complement to the
preprocess.py script. It loads the data, and the yaml file that was
dumped previously, and sticks the "old", non-unique, ids into the
file.
"""

import yaml

from typing import Tuple

from helper import *


def read_yaml_file(filename: str) -> Tuple[dict]:
    """
    Reads the yaml file that was output by the preprocessing script.

    Returns old_positions, new_positions (the dictionaries created
    by that script; see there for the documentation).
    """

    with open(filename, "r") as file:
        raw_data = yaml.load(file)

    old_positions = raw_data["old_positions"]
    new_positions = raw_data["new_positions"]

    return old_positions, new_positions


def recreate_old_array(ids: np.array, old_positions: dict) -> np.array:
    """
    Recreates the old array by performing essentially a find and replace.
    """

    ids[np.array(list(old_positions.keys()))] = np.array(list(old_positions.values()))

    return ids
