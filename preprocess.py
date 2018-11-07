"""
Pre-processes the SIMBA HDF5 data by replacing non-unique ParticleIDs with unique ones.

For usage information, use python3 preprocess.py -h
"""

import h5py
import yaml
import numpy as np

from typing import Tuple

from helper import *


def find_non_unique_ids(ids: np.array) -> Tuple[np.array]:
    """
    Takes the ID array ids, and returns two new arrays.
    
    These arrays contain the non-unique IDs, and their
    positions in the original ids array, respectively.
    """

    args = ids.argsort()
    mask = np.empty(args.shape, dtype=bool)
    sorted_ids = ids[args]

    # By definition, the first element should not be a repeat of itself.
    mask[0] = False
    # The actual duplicate check; works because sorted_ids is, well, sorted.
    mask[1:] = sorted_ids[1:] == sorted_ids[:-1]

    # sorted_ids may be very large and we no longer need it
    del sorted_ids

    # Now we need to put everything back where it belongs.
    position_corrected_mask = np.empty_like(mask)
    position_corrected_mask[args] = mask

    # Now we can compress everything to a nice integer array
    duplicate_positions = np.where(position_corrected_mask)[0]
    duplicate_ids = ids[duplicate_positions]

    return duplicate_ids, duplicate_positions


def generate_new_ids(ids: np.array, n_required: int) -> np.array:
    """
    Generates the new IDs. Assumes that all ids are contained in the
    original ids array.
    """

    current_max_id = ids.max()
    new_ids = np.arange(n_required) + current_max_id + 1

    return new_ids


def find_and_replace_non_unique_ids(ids: np.array) -> Tuple[np.array, dict]:
    """
    Finds and replacs the non-unique ids in the ids array.
    
    Returns:

    + The new ID array, and
    For the IDs that have changed:
    + A dictionary with {position_in_array: old ID}
    + A dictionary with {position_in_array: new ID}
    """

    duplicate_ids, duplicate_positions = find_non_unique_ids(ids)
    replacement_ids = generate_new_ids(ids, n_required=len(duplicate_ids))

    new_ids = ids
    new_ids[duplicate_positions] = replacement_ids

    old_position_dict = {k: v for k, v in zip(duplicate_positions, duplicate_ids)}
    new_position_dict = {k: v for k, v in zip(duplicate_positions, replacement_ids)}

    return new_ids, old_position_dict, new_position_dict


def write_data(filename: str, old_position: dict, new_position: dict) -> None:
    """
    Serialises the data from the output from find_and_replace_non_unique_ids
    to file, using yaml.
    """

    combined = {"old_positions": old_position, "new_positions": new_position}

    with open(filename, "w") as f:
        yaml.dump(combined, f)

    return


def load_hdf5_replace_and_dump(filename: str, output_filename_extra="duplicated"):
    """
    Reads the IDs from the HDF5 file at filename, concatenates all of the particle
    types into one array, finds duplicates, fixes them, saves the duplicates file,
    and writes to the original HDF5 file.
    """

    existing_particle_types, id_array_list = zip(
        *read_particle_ids_from_file(f"{filename}.hdf5").items()
    )
    id_array, insertion_points = combine_arrays(id_array_list)

    new_id_array, old_position_dict, new_position_dict = find_and_replace_non_unique_ids(
        id_array
    )

    new_id_array_list = split_arrays(new_id_array, insertion_points)

    duplicated_filename = f"{filename}_{output_filename_extra}.yml"
    write_data(duplicated_filename, old_position_dict, new_position_dict)

    write_all_id_arrays(f"{filename}.hdf5", new_id_array_list, existing_particle_types)

    return


if __name__ == "__main__":
    # Run in script mode!
    import argparse as ap

    PARSER = ap.ArgumentParser(
        description="""
        Preprocessor for halo finding on SIMBA data. SIMBA does not require unique IDs,
        and this can cause some trouble with halo finders (and other postprocessing
        tools). This python script goes through and replaces non-unique IDs in the given
        HDF5 output file, saving the diffs to file.
        """
    )

    PARSER.add_argument(
        "-i",
        "--input",
        help="""
        Input HDF5 file to preprocess, without the file extension.
        """,
        required=True,
    )

    PARSER.add_argument(
        "-o",
        "--output",
        help="""
        Extra string to add onto the output filename for the diffs. Default: duplicated
        """,
        required=False,
        default="duplicated",
    )

    ARGS = vars(PARSER.parse_args())

    load_hdf5_replace_and_dump(
        filename=ARGS["input"], output_filename_extra=ARGS["output"]
    )
