#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:02:00
#SBATCH --output=results/%x-%j.out

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
datafile=data/tinyTwitter.json
srun -n 1 python3 __main__.py {datafile}
