#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --time=0-12:00:00
#SBATCH --partition=physical

# Load required modules
module purge  
module load Python/3.7.3-spartan_gcc-8.1.0

# Launch multiple process python code
# echo "Searching for mentions"
# time srun -n 8 python3 twitter_hashtag.py -i tinyTwitter.json
# time srun -n 8 python3 twitter_hashtag.py -i bigTwitter.json 
# time srun -n 1 python3 twitter_hashtag.py -i bigTwitter.json
# time srun -n 4 python3 twitter_hashtag.py -i bigTwitter.json

