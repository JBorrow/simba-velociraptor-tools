SIMBA/VELOCIraptor Toolkit
==========================

This toolkit aims to deal with the new non-unique ID nature of the SIMBA snapshots. VELOCIraptor assumes
that all IDs are unique internally, and so writes data assuming this is the case. This is somewhat problematic
for our use-caase, as SIMBA no longer has unique IDs. This toolkit contains four main files:

+ `preprocess.py`, which loads the SIMBA HDF5 dataset and replaces the non-unique IDs with unique ones
+ `run_velociraptor.py`, which runs VELOCIraptor on the dataset
+ `postprocess.py`, which produces two new halo catalogue files which are described below.
+ `fix_particle_ids.py`, which takes the unique ID file and postprocesses it back to the original IDs.
+ `add_info_to_snapshots.py`, which takes the two halo catalogue files (one created for the galaxies,
   one for halos), and sticks that information into the snapshots.

### Requirements

These scripts have the requirements as stated in the `requirements.txt`. You can install them by running
`pip install -r requirements.txt`. To run the automated test suite, you'll also need `pytest`.

#### Compiling VELOCIraptor

Please compile VELOCIraptor without MPI support. To do this, first unload your MPI module, and then
clone the VELOICIraptor repository (https://github.com/pelahi/VELOCIraptor-STF). Change into that
directory, create a directory called `build`, and change to it. Then, run `cmake ..` and `make`. This
will create a binary called `stf` that you will need to place wherever your `submit.slurm` script is.

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

### Snapshot Information

The final script, `add_info_to_snaphots.py` takes the halo catalogues that are created and puts the
information in the snaphots. This is held under each particle type, making the snapshot structure
as follows:

```
Header/
    ...
PartType0/
    Coordinates/
        <3 x N>
    ParticleIDs/
        <N>
    ...
    VRGalID/
        <N>
    VRHaloID/
    	<N>
...
PartType5/
    Coordinates/
        <3 x N>
    ParticleIDs/
        <N>
    ...
    VRGalID/
        <N>
    VRHaloID/
    	<N>
```
with `VRGalID` and `VRHaloID` storing, for each particle, the galaxy and halo that it belongs to
respectively. Particles that live outside halos have an ID of `-1`.
