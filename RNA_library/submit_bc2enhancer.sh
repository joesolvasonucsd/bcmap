#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:bc2enhancer_rnabc-br2_1-weidict
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=6:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-br2_1-weidict//stdout/bc2enhancer_rnabc-br2_1-weidict.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-br2_1-weidict//stderr/bc2enhancer_rnabc-br2_1-weidict.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 2.bc2enhancer_random-Bkgd.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-br2_1-weidict// ../../../data/otxa-sequencing-data/bc-enhancer-dictionaries/_dicts/MLOTX-wei-dicts/MLOTXA-wei-dict// 1 4 bc2enhancer_rnabc-br2_1-weidict