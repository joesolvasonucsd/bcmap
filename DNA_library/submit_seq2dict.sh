#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=seq2dict_MLOTXBi12_TTG
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=48:00:00
#SBATCH --output=./stdout/MLOTXBi12_TTG.out.txt
#SBATCH --error=./stderr/MLOTXBi12_TTG.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library//seq2dict_v2.4_inverse_joe.py ./ ./split/MLOTXBi12_collapsed_filtered_collapsed_TTG.txt