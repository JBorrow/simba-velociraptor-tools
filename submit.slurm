#!/bin/bash

# Example submission script.
#SBATCH -J SIMBA-VELOCIRAPTOR
#SBATCH -N 1
#SBATCH -o halofind_%j.out
#SBATCH -e halofind_%j.err
#SBATCH -p PARTITION
#SBATCH -A GROUP
#SBATCH --exclusive
#SBATCH -t 1:00:00

snapname=""
dirname="."
velociraptortoolsdir="simba-velociraptor-tools"

python3 -u $velociraptortoolsdir/preprocess.py -i $snapname -d $dirname

python3 -u $velociraptortoolsdir/run_velociraptor.py \
        -i $snapname \
        -d $dirname \
        -t 16 \
        -C $velociraptortoolsdir/velociraptor.cfg \

python3 -u $velociraptortoolsdir/postprocess.py -i $snapname -d $dirname

python3 -u $velociraptortoolsdir/fix_particle_ids.py -i $snapname -d $dirname