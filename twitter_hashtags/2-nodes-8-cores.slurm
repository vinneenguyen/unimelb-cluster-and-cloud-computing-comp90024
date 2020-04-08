#!/bin/bash
#SBATCH --partition=physical
#SBATCH --nodes=2

#SBATCH --ntasks-per-node=4
#SBATCH --time=00:02:00
#SBATCH --output=results/%x-%j.out

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
time srun -n 8 python3 __main__.py "$DATAFILE"  # $DATAFILE passed from sbatch command


# Use this command to set parameters w/o modifying the script
# sbatch --time=$time --export=ALL,DATAFILE=data/$file --job-name=$script-$file $script
