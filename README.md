SIMBA/VELOCIraptor Toolkit
==========================

This toolkit aims to deal with the new non-unique ID nature of the SIMBA snapshots. VELOCIraptor assumes
that all IDs are unique internally, and so writes data assuming this is the case. This is somewhat problematic
for our use-caase, as SIMBA no longer has unique IDs. This toolkit contains four main files:

+ `preprocess.py`, which loads the SIMBA HDF5 dataset and replaces the non-unique IDs with unique ones
+ `run_velociraptor.sh`, which runs VELOCIraptor on the dataset
+ `postprocess.py`, which produces two new halo catalogue files which are described below.
+ `fix_particle_ids.py`, which takes the unique ID file and postprocesses it back to the original IDs.

### Requirements

These scripts have the requirements as stated in the `requirements.txt`. You can install them by running
`pip install -r requirements.txt`. To run the automated test suite, you'll also need `pytest`.

### New Halo Catalogue File

The VELOCIraptor halo finder produces a `catalog_particles` file which lists the IDs of all of the particles
that are in groups. This is useful, but an easier to use format is to simply store the group ID for all
particles in the order that they are in the snapshot file.

The above creates a `ordered_group_particles` file, that has the following structure:
```
PartTypeX/
    GroupID: [...]
```
which stores the Group ID for each particle. This can then be parsed much more quickly, e.g. for the 
Lagrangian Transfer stuff that we do.