#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=mergeFiles_/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/MLOTXAi12_collapsed_filtered_collapsed.txt_/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/MLOTXAi6_collapsed_filtered_collapsed.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=20:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/stdout/MLOTXA-with-Ns.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/stderr/MLOTXA-with-Ns.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
python 1.5.combineCollapsedFiles.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/ MLOTXA-with-Ns /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/MLOTXAi12_collapsed_filtered_collapsed.txt /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/bc-enhancer-dictionaries/_successful-runs/MLOTXA-with-Ns/MLOTXAi6_collapsed_filtered_collapsed.txt