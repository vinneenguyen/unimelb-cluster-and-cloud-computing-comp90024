#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=00:02:00
#SBATCH --output=results/%x-%j.out

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
time srun -n 8 python3 __main__.py "$DATAFILE"  # $DATAFILE passed from sbatch command


# Use these commands to run script on different data files w/o modifying the script
# mkdir -p results  # create output directory if not exist
# script=<path to slurm script>
# file=<path to data file>
# sbatch --job-name=${script##*/}-${file##*/} --export=ALL,DATAFILE=$file $script
