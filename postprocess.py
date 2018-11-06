"""
Postprocess the SIMBA and VELOCIraptor outputs into new files that describe
the particles contained in each halo by _position in the file_ rather than
particle ID.

This script also fixes-up the SIMBA output file to ensure that it has the
original IDs (i.e. the ones that may be duplicated).
"""

import numpy as np
import h5py

from typing import Tuple


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


def load_velociraptor_data(filename: str) -> np.array:
    """
    Loads the velociraptor data.
    
    Give filename the path without the .<> file, as we need multiple.

    Returns the ID array of particle IDs, and the "group size" array for
    each group.
    """

    with h5py.File(f"{filename}.catalog_particles", "r") as handle:
        particle_ids = handle["Particle_IDs"][...]

    with h5py.File(f"{filename}.catalog_groups", "r") as handle:
        group_sizes = handle["Group_Size"][...]

    return particle_ids, group_sizes


def create_group_array(group_sizes: np.array) -> np.array:
    """
    Creates an array that looks like:

    [GroupID0, GroupID0, ..., GroupIDN, GroupIDN]

    i.e. for each group create the correct number of group ids.

    This is used to be sorted alongside the particle IDs to track
    the placement of group IDs.
    """

    slices = []
    running_total_of_particles = 0

    for group in group_sizes:
        slices.append([running_total_of_particles, group + running_total_of_particles])
        running_total_of_particles += group

    groups = np.empty(group_sizes.sum(), dtype=int)

    for group_id, group in enumerate(slices):
        groups[group[0] : group[1]] = group_id

    return groups


def read_particle_ids_from_file(filename: str) -> Tuple[dict]:
    """
    Reads the particle IDs from file. Stores them in a dictionary
    with the particle type corresponding to the index, i.e.

    {
        0: <pids for PartType0,
        ...
    }

    Also returns a similar dictionary that gives the _position_ in the
    file for those particles.
    """

    particle_ids = {}

    with h5py.File(filename, "r") as handle:
        for ptype in range(6):
            try:
                particle_ids[ptype] = handle[f"/PartType{ptype}/ParticleIDs"][...]
            except KeyError:
                pass

    positions = {}

    for ptype, ids in particle_ids.items():
        positions[ptype] = np.arange(len(ids.shape))

    return particle_ids, positions


def create_positions_groups_correspondance(
    particle_ids_velociraptor: np.array,
    group_array_velociraptor: np.array,
    particle_ids_snapshot: dict,
):
    """
    Returns a dictionary, similar to positions_snapshot, i.e. that each contains
    the particle types, but that it contains the group ids ordered by the original
    position in the HDF5 file. 
    """

    groups_snapshot = {}

    for ptype, particle_ids in particle_ids_snapshot.items():
        _, indices_v, indices_p = np.intersect1d(
            particle_ids_velociraptor,
            particle_ids,
            assume_unique=True,
            return_indices=True,
        )

        groups_in_order = np.empty(particle_ids.shape, dtype=int)
        # Particles outside of groups have -1 as a groupid
        groups_in_order[...] = -1

        groups_in_order[indices_p] = group_array_velociraptor[indices_v]

        groups_snapshot[ptype] = groups_in_order

    return groups_snapshot


def write_ordered_groups_to_file(filename: str, groups_snapshot: dict):
    """
    Writes the ordered groups to a HDF5 file with filename.
    """

    with h5py.File(filename, "w") as handle:
        for ptype, particle_groups in groups_snapshot.items():
            current_group = handle.create_group(f"PartType{ptype}")
            current_group.create_dataset(f"GroupID", data=particle_groups)

    return


def load_data_and_write_new_catalog(
    snapshot_filename: str, catalogue_path: str
) -> None:
    """
    Load the data in from file, parse it, and write out the new catalogue.
    """

    velociraptor_particle_ids, velociraptor_group_sizes = load_velociraptor_data(
        catalogue_path
    )
    group_array = create_group_array(velociraptor_group_sizes)

    particle_ids, _ = read_particle_ids_from_file(snapshot_filename)

    groups_snapshot = create_positions_groups_correspondance(
        velociraptor_particle_ids, group_array, particle_ids
    )

    write_ordered_groups_to_file(
        filename=f"{catalogue_path}.ordered_group_particles",
        groups_snapshot=groups_snapshot,
    )

    return


if __name__ == "__main__":
    import argparse as ap

    PARSER = ap.ArgumentParser(
        description="""
        Postprocessor for halo finding on SIMBA data. This creates a new file
        alongside the halo finder data that describes the groups that each
        particle is in _in the same order as the particles in the file_.
        This makes a lot of things much easier.

        It also (TBD) fixes up the original file to make the IDs non-unique
        again.
        """
    )

    PARSER.add_argument(
        "-i",
        "--input",
        help="Input snapshot filename. This should be provided WITHOUT the .hdf5. Required.",
        required=True,
    )

    PARSER.add_argument(
        "-o",
        "--output",
        help="""
        The prepended path to your velociraptor output. For example, if you
        give ./halo/output, you will get a bunch of files like ./halo/output.particles,
        .catalogue... etc. Default is ./halo/<snapshot_filename_without_.hdf5>.
        """,
        required=False,
        default="DEFAULT",
    )

    ARGS = vars(PARSER.parse_args())

    if ARGS["input"][-5:] == ".hdf5":
        raise InputError(
            "Please remove the .hdf5 at the end of your snapshot input filename, this is added automatically by VELOCIraptor."
        )

    if ARGS["output"] == "DEFAULT":
        # Set to the actual default option.
        ARGS["output"] = f"halo/{ARGS['input']}"

    load_data_and_write_new_catalog(
        snapshot_filename=f"{ARGS['input']}.hdf5",
        catalogue_path=ARGS["output"]
    )
