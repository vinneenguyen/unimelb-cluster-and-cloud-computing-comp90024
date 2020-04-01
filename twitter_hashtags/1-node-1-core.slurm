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
<<<<<<< HEAD
srun -n 1 python3 __main__.py -i data/tinyTwitter.json
#srun -n 1 python3 __main__.py -i data/tinyTwitter.json
=======
srun -n 1 python3 __main__.py data/tinyTwitter.json
>>>>>>> 68dadde4e851168417b28e2e537d222c9d1fc005
# time srun -n 1 python3 __main__.py -i data/bigTwitter.json
