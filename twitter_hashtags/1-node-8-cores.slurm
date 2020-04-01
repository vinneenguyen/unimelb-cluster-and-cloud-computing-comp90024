#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --time=00:02:00
#SBATCH --nodes=1
#SBATCH --ntasks=8

# Load required modules
#module purge # restore default modules
module load Python/3 # latest Python 3

# Launch multiple process python code
time srun -n 8 python3 __main__.py -i tinyTwitter.json
#time srun -n 8 python3 __main__.py -i smallTwitter.json
# time srun -n 8 python3 __main__.py -i bigTwitter.json
