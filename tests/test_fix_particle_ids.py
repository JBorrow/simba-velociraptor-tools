"""
Tests for the functions in fix_particle_ids.py
"""

from fix_particle_ids import *
from preprocess import *


def test_find_and_replace_backwards_0():
    """
    Tests the find and replace in the other direction this time!
    """
    data = np.array([7, 5, 3, 2, 4, 5, 6, 2, 1, 7])

    new_ids, oldpos, newpos = find_and_replace_non_unique_ids(data)

    data_recreated = recreate_old_array(new_ids, oldpos)

    assert (data == data_recreated).all()
