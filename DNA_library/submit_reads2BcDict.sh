#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=read2collapsed-MLOTXBi12
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=4G
#SBATCH --time=1:00:00
#SBATCH --output=./stdout/MLOTXBi12.out.txt
#SBATCH --error=./stderr/MLOTXBi12.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/1.reads2collapsed.sh ./ MLOTXBi12 /oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/