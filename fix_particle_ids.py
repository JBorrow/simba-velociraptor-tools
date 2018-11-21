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

    indices = np.array(list(old_positions.keys()))
    values = np.array(list(old_positions.values()))

    if indices.size == 0:
        print(
            "We don't need to fix anything; you never had any duplicated IDs in the first place!"
        )
        exit(0)
    else:
        ids[indices] = values

        return ids


def open_fix_and_write(snapshot: str, replaced: str):
    """
    Takes the two filenames, the snapshot filename and the filename
    of the replacement file (yaml).

    This opens those two files and fixes-up the ID array in the original
    snapshot back to how it originally was.
    """

    existing_particle_types, original_id_list = zip(
        *read_particle_ids_from_file(snapshot).items()
    )

    old_positions, _ = read_yaml_file(replaced)

    combined_ids, insertion_points = combine_arrays(original_id_list)

    old_array = recreate_old_array(combined_ids, old_positions)

    new_id_list = split_arrays(old_array, insertion_points)

    write_all_id_arrays(snapshot, new_id_list, existing_particle_types)

    return


if __name__ == "__main__":
    # Run in script mode!
    import argparse as ap

    PARSER = ap.ArgumentParser(
        description="""
        Returns the particle IDs back to normal. This takes the exact same arguments
        that you passed to preprocess.py.
        """
    )

    PARSER.add_argument(
        "-i",
        "--input",
        help="""
        Input HDF5 file to preprocess, without the file extension. Required.
        """,
        required=True,
    )

    PARSER.add_argument(
        "-d",
        "--directory",
        help="""
        Directory that the snapshots and halos should live in. Required.
        """,
        required=True,
    )

    PARSER.add_argument(
        "-o",
        "--output",
        help="""
        Extra string to add onto the output filename for the diffs.
        """,
        required=False,
        default="duplicated",
    )

    ARGS = vars(PARSER.parse_args())

    filename = f"{ARGS['directory']}/{ARGS['input']}.hdf5"
    duplicated_filename = f"{ARGS['directory']}/{ARGS['input']}_{ARGS['output']}.yml"

    open_fix_and_write(filename, duplicated_filename)
