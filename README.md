SIMBA/VELOCIraptor Toolkit
==========================

This toolkit aims to deal with the new non-unique ID nature of the SIMBA snapshots. VELOCIRaptor assumes
that all IDs are unique internally, and so writes data assuming this is the case. This is somewhat problematic
for our use-caase, as SIMBA no longer has unique IDs. This toolkit contains three main files:

+ `preprocess.py`, which loads the SIMBA HDF5 dataset and replaces the non-unique IDs with unique ones
+ `run_velociraptor.sh`, which runs VELOCIRaptor on the dataset
+ `postprocess.py`, which fixes the SIMBA HDF5 dataset back up to it's original status, and produces
  two new halo catalogue files which are described below.

### Requirements

These scripts have the requirements as stated in the `requirements.txt`. You can install them by running
`pip install -r requirements.txt`. To run the automated test suite, you'll also need `pytest`.