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

python3 -u simba-velociraptor-tools/preprocess.py -i $snapname

python3 -u simba-velociraptor-tools/run_velociraptor.py \
        -i $snapname \
        -t 16 \
        -C simba-velociraptor-tools/velociraptor.cfg \

python3 -u simba-velociraptor-tools/postprocess.py -i $snapname

python3 -u simba-velociraptor-tools/fix_particle_ids.py -i $snapname