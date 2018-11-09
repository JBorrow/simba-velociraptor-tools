"""
Tests the functions in postprocess.py
"""

from postprocess import *


def test_create_group_array_0():
    """
    Tests the group array creation.
    """

    group_sizes = np.array([5, 10, 20])

    # Why don't we just do this?
    expected_output = np.concatenate(
        [np.repeat(group_id, n) for group_id, n in enumerate([5, 10, 20])]
    )

    output = create_group_array(group_sizes)

    assert (output == expected_output).all()


def test_create_positions_roups_correspondance_0():
    """
    Tests the complex behaviour of the group correspondance.
    """

    particle_ids_velociraptor = np.array([1, 2, 5, 3, 4, 9, 8, 10, 17])

    group_array_velociraptor = np.array([0, 7, 7, 7, 4, 2, 1, 1, 1])

    particle_ids_snapshot = {
        0: np.array([2, 5, 11, 15, 26, 9, 8]),
        1: np.array([17, 1, 3, 6, 4, 10]),
    }

    expected_group_array = {
        0: np.array([7, 7, -1, -1, -1, 2, 1]),
        1: np.array([1, 0, 7, -1, 4, 1]),
    }

    groups_snapshot = initialise_groups_dictionary(particle_ids_snapshot)

    groups_snapshot = create_positions_groups_correspondance(
        particle_ids_velociraptor,
        group_array_velociraptor,
        particle_ids_snapshot,
        groups_snapshot,
    )

    for g, e_g in zip(groups_snapshot.values(), expected_group_array.values()):
        assert (g == e_g).all()
