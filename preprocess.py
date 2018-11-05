"""
Pre-processes the SIMBA HDF5 data by replacing non-unique ParticleIDs with unique ones.

For usage information, use python3 preprocess.py -h
"""

import h5py
import yaml
import numpy as np

from typing import Tuple


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


def combine_arrays(id_array_list: list) -> Tuple[np.ndarray, list]:
    """
    Combines the arrays in id_array_list into one long array and returns
    the long array along with the indicies at which things were concatenated
    together.
    """

    insertion_points = [0]

    for index, array in enumerate(id_array_list):
        insertion_points.append(insertion_points[index] + array.shape[0])

    out_array = np.concatenate(id_array_list)

    return out_array, insertion_points


def split_arrays(id_array: np.array, insertion_points: list) -> list:
    """
    Splits the array that was combined previously by combine_arrays.
    """

    slices = [[x, y] for x, y in zip(insertion_points[:-1], insertion_points[1:])]

    id_array_list = []

    for slice in slices:
        id_array_list.append(id_array[slice[0] : slice[1]])

    return id_array_list


def load_hdf5_replace_and_dump(filename: str, output_filename_extra="duplicated"):
    """
    Reads the IDs from the HDF5 file at filename, concatenates all of the particle
    types into one array, finds duplicates, fixes them, saves the duplicates file,
    and writes to the original HDF5 file.
    """

    return
