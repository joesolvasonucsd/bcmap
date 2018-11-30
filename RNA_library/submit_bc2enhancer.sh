#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:bc2enhancer_sci-rnabc-i12
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=4:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/stdout/bc2enhancer_sci-rnabc-i12.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/stderr/bc2enhancer_sci-rnabc-i12.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 2.bc2enhancer_random-Bkgd.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/science-2015-rnaseq-normal/rnabc-i12/ ../../../data/otxa-sequencing-data/bc-enhancer-dictionaries/_dicts/MLOTXA-dict// 1 4 bc2enhancer_sci-rnabc-i12