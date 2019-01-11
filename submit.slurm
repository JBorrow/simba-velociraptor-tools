#!/bin/bash

# Example submission script.
#SBATCH -J SIMBA-VELOCIRAPTOR
#SBATCH -N 1
#SBATCH -o halofind_%j.out
#SBATCH -e halofind_%j.err
#SBATCH -p PARTITION
#SBATCH -A GROUP
#SBATCH --exclusive
#SBATCH -t 8:00:00

snapname=""
dirname="."
velociraptortoolsdir="simba-velociraptor-tools"

python3 -u $velociraptortoolsdir/preprocess.py -i $snapname -d $dirname

# Run the halo finder

python3 -u $velociraptortoolsdir/run_velociraptor.py \
        -i $snapname \
        -d $dirname \
        -t 16 \
        -C $velociraptortoolsdir/velociraptor.cfg \

# Run velociraptor in galaxy finder mode

python3 -u $velociraptortoolsdir/run_velociraptor.py \
        -i $snapname \
        -d $dirname \
        -t 16 \
        -c galaxy \
        -C $velociraptortoolsdir/velociraptor_galaxy.cfg \

# Postprocess both the galaxy and halo catalogue

python3 -u $velociraptortoolsdir/postprocess.py -i $snapname -d $dirname

python3 -u $velociraptortoolsdir/postprocess.py \
        -i $snapname \
        -d $dirname \
        -c galaxy

python3 -u $velociraptortoolsdir/fix_particle_ids.py -i $snapname -d $dirname
