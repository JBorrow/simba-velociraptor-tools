"""
Tests the functions in preprocess.py
"""

from preprocess import *
import os


def test_find_non_unique_ids_0():
    """
    Tests the null case, i.e. no repeated ids.
    """
    data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    repeated, positions = find_non_unique_ids(data)

    assert repeated.shape == (0,)
    assert positions.shape == (0,)

    return


def test_find_non_unique_ids_1():
    """
    Tests the null reversed case, i.e. no repeated ids.
    """
    data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])[::-1]

    repeated, positions = find_non_unique_ids(data)

    assert repeated.shape == (0,)
    assert positions.shape == (0,)

    return


def test_find_non_unique_ids_2():
    """
    Tests the perfect case where everything is repeated.
    """
    data = np.array([1234132, 1234132, 1234132, 1234132, 1234132])

    repeated, positions = find_non_unique_ids(data)

    assert (repeated == np.array([1234132, 1234132, 1234132, 1234132])).all()
    assert (positions == np.array([1, 2, 3, 4])).all()

    return


def test_find_non_unique_ids_3():
    """
    Tests a more realistic case.
    """
    data = np.array([7, 5, 3, 2, 4, 5, 6, 2, 1, 7])

    repeated, positions = find_non_unique_ids(data)

    assert (repeated == np.array([5, 2, 7])).all()
    assert (positions == np.array([5, 7, 9])).all()

    return


def test_generate_new_ids_0():
    """
    Tests the generation of new IDs.
    """
    data = np.arange(10)
    n_required = 10
    expected_output = np.arange(10, 20, 1)

    assert (expected_output == generate_new_ids(data, n_required)).all()

    return


def test_find_and_replace_0():
    """
    Tests a more realistic case.
    """
    data = np.array([7, 5, 3, 2, 4, 5, 6, 2, 1, 7])

    new_ids, oldpos, newpos = find_and_replace_non_unique_ids(data)

    expected_new_ids = np.array([7, 5, 3, 2, 4, 8, 6, 9, 1, 10])

    expected_oldpos = {5: 5, 7: 2, 9: 7}
    expected_newpos = {5: 8, 7: 9, 9: 10}

    assert (new_ids == expected_new_ids).all()
    assert expected_oldpos == oldpos
    assert expected_newpos == newpos

    return


def test_write_data_0():
    """
    Tests the writing of the data.
    """

    newpos = {4: 7, 5: 8, 6: 9}
    oldpos = {4: 1, 5: 2, 6: 3}

    write_data("test.yml", oldpos, newpos)

    # Let's load it back in
    with open("test.yml", "r") as f:
        data = yaml.load(f)

    # Delete our friendly neighbourhood test file
    os.remove("test.yml")

    expected_data = {"old_positions": oldpos, "new_positions": newpos}

    assert expected_data == data


def test_combine_and_split_0():
    """
    Tests the combine_array and split_array functions.
    """

    data_in = [np.arange(100), np.arange(10), np.zeros(1000)]

    data_out = split_arrays(*combine_arrays(data_in))

    for d_in, d_out in zip(data_in, data_out):
        assert (d_in == d_out).all()

    return
