"""
Pre-processes the SIMBA HDF5 data by replacing non-unique ParticleIDs with unique ones.

For usage information, use python3 preprocess.py -h
"""

import h5py
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

