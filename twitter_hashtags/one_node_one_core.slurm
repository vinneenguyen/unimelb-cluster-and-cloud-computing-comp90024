#!/bin/bash
#SBATCH --partition=physical
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1

# Load required modules
module load Python/3.5.2-goolf-2015a 

# Launch multiple process python code
srun -n 1 main
