#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=00:02:00

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
time srun -n $SLURM_NTASKS python3 __main__.py "$DATAFILE"  # $DATAFILE passed from sbatch command


# Use these commands to run job script with different parameters
# mkdir -p results  # create output directory if not exist
# nodes=<number of nodes>
# ntasks=<number of tasks>
# time=<time limit for job>
# file=<path to data file>
# script=<path to job script>
# sbatch --nodes=$nodes --ntasks=$ntasks --time=$time --export=ALL,DATAFILE=$file --output=results/${nodes}n${ntasks}c-${file##*/}-%j.out $script
