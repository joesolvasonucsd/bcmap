#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=split4parallel_MLOTXBi12_collapsed_filtered_collapsed
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=48:00:00
#SBATCH --output=./stdout/MLOTXBi12_collapsed_filtered_collapsed.out.txt
#SBATCH --error=./stderr/MLOTXBi12_collapsed_filtered_collapsed.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/2.collapsed2dict.sh seq2dict_v2.4_inverse_joe.py ./ ./MLOTXBi12_collapsed_filtered_collapsed.txt solvason@ucsd.edu 30 48 /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/