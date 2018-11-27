#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=seq2dict_MLOTXAi6_NGG
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=12:00:00
#SBATCH --output=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stdout/MLOTXAi6_NGG.out.txt
#SBATCH --error=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stderr/MLOTXAi6_NGG.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python seq2dict_v2.4.py ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/ ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/split/MLOTXAi6_collapsed_filtered_collapsed_NGG.txt