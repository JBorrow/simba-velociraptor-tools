"""
This script takes the information available in the reduced files
(i.e. the galaxies and halo particle data) and places it inside the
snapshots for easy storage and compatibility. The galaxy IDs are
stored as VRGalID and halo ids as VRHaloID.
"""

import yaml

from typing import Tuple

from helper import *


def read_from_hdf_file(filename: str, handle: str):
    """
    Reads the item from the file by opening it temporarily.
    """

    with h5py.File(filename, "r") as file:
        return file[handle][...]


def write_to_hdf_file(filename: str, handle: str, data):
    """
    Writes the data to HDF5 file creating the handle if it needs to be
    created.
    """

    with h5py.File(filename) as file:
        file.create_dataset(handle, data=data)

    return


def read_and_write_all(catalog_filename, snapshot_filename, name: str):
    """
    Reads and writes all particle types.

    Name should be the name of the dataset you want to be
    created in PartType<X>/ that contains the IDs.
    """

    with h5py.File(snapshot_filename, "r") as file:
        particle_numbers = file["Header"].attrs["NumPart_Total"]

    for particle_type, number in zip([0, 1, 4, 5], particle_numbers):
        if not number:
            # If there are none of that particle then skip it
            continue

        ids = read_from_hdf_file(catalog_filename, f"PartType{particle_type}/GroupID")

        write_to_hdf_file(snapshot_filename, f"PartType{particle_type}/{name}")
        
    return


if __name__ == "__main__":
    # Run in script mode!
    import argparse as ap

    PARSER = ap.ArgumentParser(
        description="""
        Takes the two ordered_groups_particles files (one for galaxies and
        one for halos) and places them into the HDF5 snapshot file under
        VRHaloID and VRGalID.
        """
    )

    PARSER.add_argument(
        "-s",
        "--snapshot",
        help="""
        Snapshot filename (including path, but excluding .hdf5).
        Example: /path/to/snapshot/snap_hm58_1234. Required.
        """,
        required=True
    )

    PARSER.add_argument(
        "-v",
        "--halos",
        help="""
        Path to the .ordered_group_particles file for Halos. Required.
        """,
        required=True
    )

    PARSER.add_argument(
        "-g",
        "--galaxies",
        help="""
        Path to the .ordered_group_particles file for Galaxies.
        """,
        required=False,
        default=None
    )

    ARGS = vars(PARSER.parse_args())

    snapshot = f"{ARGS['snapshot']}.hdf5"

    read_and_write_all(ARGS["halos"], snapshot, "VRHaloID")

    if ARGS["galaxies"] is not None:
        read_and_write_all(ARGS["galaxies"], snapshot, "VRGalID")


