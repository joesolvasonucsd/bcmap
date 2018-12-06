#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=seq2dict_test_NTA
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=15G
#SBATCH --time=1:00:00
#SBATCH --output=./stdout/test_NTA.out.txt
#SBATCH --error=./stderr/test_NTA.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library//seq2dict_v2.4.py ./ ./split/test_merge_merged_NTA.txt