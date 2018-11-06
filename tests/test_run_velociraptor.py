"""
Tests the path functions in run_velociraptor.
"""

from run_velociraptor import *


def test_parse_output_path_0():
    """
    Tests the parsing of the output path when no path is given.
    """

    path = "test.md"
    file, directory = parse_output_path(path)

    assert file == "test.md"
    assert directory == "."


def test_parse_output_path_1():
    """
    Tests a more complex path.
    """

    path = "./gonna/do/some/things/hsdf.hdf5"

    file, directory = parse_output_path(path)

    assert file == "hsdf.hdf5"
    assert directory == "gonna/do/some/things"
