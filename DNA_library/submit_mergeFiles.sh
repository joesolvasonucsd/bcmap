#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=mergeFiles_./MLOTXBi12_collapsed_filtered_collapsed.txt_./MLOTXBi12_collapsed_filtered_collapsed.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=10G
#SBATCH --time=1:00:00
#SBATCH --output=./stdout/test_merge.out.txt
#SBATCH --error=./stderr/test_merge.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
python /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/1.5.combineCollapsedFiles.py ./ test_merge ./MLOTXBi12_collapsed_filtered_collapsed.txt ./MLOTXBi12_collapsed_filtered_collapsed.txt