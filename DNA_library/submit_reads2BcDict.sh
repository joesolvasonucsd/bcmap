#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=read2collapsed-MLOTXAi6
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=4:00:00
#SBATCH --output=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stdout/MLOTXAi6.out.txt
#SBATCH --error=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/stderr/MLOTXAi6.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash 1.reads2collapsed.sh ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/MLOTXAi6-with-Ns/ MLOTXAi6