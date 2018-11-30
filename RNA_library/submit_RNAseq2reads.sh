#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:sci-rnabc-i12
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=4:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/stdout/sci-rnabc-i12.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/stderr/sci-rnabc-i12.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 1.RNAseq2reads.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/ /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/MLOTXAFnBR3i12_collapsed_filtered_collapsed.txt