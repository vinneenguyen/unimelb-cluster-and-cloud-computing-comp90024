#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=00:02:00
#SBATCH --output=results/1-node-8-cores-%j.out

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
srun -n 8 python3 __main__.py data/tinyTwitter.json
#srun -n 8 python3 __main__.py data/smallTwitter.json
#srun -n 8 python3 __main__.py data/bigTwitter.json
