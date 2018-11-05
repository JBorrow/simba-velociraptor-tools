"""
Tests the functions in preprocess.py
"""

from preprocess import *

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