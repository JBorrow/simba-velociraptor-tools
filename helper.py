"""
Some helper functions that deal with the splitting and re-forming
of particle ID arrays.
"""

import numpy as np

from typing import Tuple


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
