#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:02:00
#SBATCH --output=results/1-node-1-core-%j.out

# Load required modules
#module purge # restore default modules
module load Python/3 # latest Python 3

# Launch multiple process python code
srun -n 1 python3 __main__.py -i tinyTwitter.json
# time srun -n 1 python3 __main__.py -i bigTwitter.json
