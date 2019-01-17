"""
This python script runs velociraptor on a given snapshot.

This is a really thin wrapper, but is nicely shell-agnostic, and the function
run_velociraptor can be scripted.
"""

import os
import pathlib

from typing import Tuple


class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


def run_velociraptor(
    snapshot_filename: str,
    velociraptor_path: str,
    output_path: str,
    omp_num_threads: int,
    velociraptor_options_file_path="velociraptor.cfg",
) -> None:
    """
    Runs VELOCIRAPTOR with omp_num_threads.
    """

    if omp_num_threads != -1:
        os.environ["OMP_NUM_THREADS"] = f"{omp_num_threads}"

    os.system(
        " ".join(
            [
                velociraptor_path,
                "-I 2",
                "-i",
                snapshot_filename,
                "-C",
                velociraptor_options_file_path,
                "-o",
                output_path,
            ]
        )
    )


def parse_output_path(output_path: str) -> Tuple[str]:
    """
    Parses the output path into the "filename" bit, and the
    pre-pended path bit.

    Returns filename, pathname
    """

    path = pathlib.Path(output_path)

    return str(path.name), str(path.parent)


def create_directory_if_not_exists(dir: str) -> None:
    """
    Creates the directory dir if it doesn't exist.
    """

    if not os.path.exists(dir):
        os.makedirs(dir)

    return


if __name__ == "__main__":
    import argparse as ap

    PARSER = ap.ArgumentParser(
        description="""
        A very thin wrapper around VELOCIraptor in python. Used for scripting.
        You will need to have pre-compiled velociraptor, and found the stf
        binary. You should compile VELOCIraptor without MPI, but with OMP
        support.
        """
    )

    PARSER.add_argument(
        "-v",
        "--velociraptor",
        help="""
        The path to the velociraptor stf binary. Defaults to "./stf".
        """,
        required=False,
        default="./stf",
    )

    PARSER.add_argument(
        "-o",
        "--output",
        help="""
        The prepended path to your velociraptor output. For example, if you
        give ./halo/output, you will get a bunch of files like ./halo/output.particles,
        .catalogue... etc. Default is ./{-c}/<snapshot_filename_without_.hdf5>.
        """,
        required=False,
        default="DEFAULT",
    )

    PARSER.add_argument(
        "-i",
        "--input",
        help="Input snapshot filename. This should be provided WITHOUT the .hdf5. Required.",
        required=True,
    )

    PARSER.add_argument(
        "-d",
        "--directory",
        help="""
        Directory that the snapshots and halos should live in. Required.
        """,
        required=True,
    )

    PARSER.add_argument(
        "-t",
        "--threads",
        help="""
        Number of OMP threads to use. If not set, then this will use the current
        default on your system.
        """,
        required=False,
        default="-1",
    )

    PARSER.add_argument(
        "-C",
        "--config",
        help="""
        Velociraptor configuration file. If not set, this defaults to 
        velociraptor.cfg which is in this directory.
        """,
        required=False,
        default="velociraptor.cfg",
    )

    PARSER.add_argument(
        "-c",
        "--catalogue",
        help="""
        Name of the catalogue (i.e. the directory that it exists in). Defaults
        to 'halo'.
        """,
        required=False,
        default="halo"
    )


    ARGS = vars(PARSER.parse_args())

    # Quick check to see if they have accidentally included the HDF5

    if ARGS["input"][-5:] == ".hdf5":
        raise InputError(
            "Please remove the .hdf5 at the end of your snapshot input filename, this is added automatically by VELOCIraptor."
        )

    if ARGS["output"] == "DEFAULT":
        # Set to the actual default option.
        ARGS["output"] = f"{ARGS['catalogue']}/{ARGS['input']}"

    # Create the halo directory if required.
    filename, directory = parse_output_path(ARGS["output"])
    create_directory_if_not_exists(f"{ARGS['directory']}/{directory}")

    runtime_options = dict(
        snapshot_filename=f"{ARGS['directory']}/{ARGS['input']}",
        velociraptor_path=ARGS["velociraptor"],
        output_path=f"{ARGS['directory']}/{ARGS['output']}",
        omp_num_threads=int(ARGS["threads"]),
        velociraptor_options_file_path=ARGS["config"],
    )

    run_velociraptor(**runtime_options)
