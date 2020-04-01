#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --time=00:02:00
#SBATCH --nodes=2
#SBATCH --ntasks=8

# Load required modules
#module purge # restore default modules
module load Python/3 # latest Python 3

# Launch multiple process python code
time srun -n 8 python3 __main__.py -i tinyTwitter.json
# time srun -n 8 python3 __main__.py -i bigTwitter.json

#!/bin/bash
#SBATCH --partition=cloud
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=00:02:00
#SBATCH --output=results/2-nodes-8-cores-%j.out

# Load required modules
module load Python/3 # latest Python 3

# Launch multiple process python code
srun -n 8 python3 __main__.py data/tinyTwitter.json
#srun -n 8 python3 __main__.py data/smallTwitter.json
#srun -n 8 python3 __main__.py data/bigTwitter.json
