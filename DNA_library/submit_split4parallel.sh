#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=split4parallel_MLOTXAi6_collapsed_filtered_collapsed
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=12:00:00
#SBATCH --output=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stdout/MLOTXAi6_collapsed_filtered_collapsed.out.txt
#SBATCH --error=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stderr/MLOTXAi6_collapsed_filtered_collapsed.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash 2.collapsed2dict_seq2dict_v2.4.sh ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/ ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/MLOTXAi6_collapsed_filtered_collapsed.txt solvason@ucsd.edu 30 12