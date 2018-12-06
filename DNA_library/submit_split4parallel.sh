#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=split4parallel_test_merge_merged
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=15G
#SBATCH --time=1:00:00
#SBATCH --output=./stdout/test_merge_merged.out.txt
#SBATCH --error=./stderr/test_merge_merged.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/2.collapsed2dict.sh seq2dict_v2.4.py ./ ./test_merge_merged.txt solvason@ucsd.edu 15 1 /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/