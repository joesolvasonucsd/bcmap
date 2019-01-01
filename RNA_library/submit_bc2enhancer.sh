#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:bc2enhancer_ke2018-rna-dna-norm-br3
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=1:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict//stdout/bc2enhancer_ke2018-rna-dna-norm-br3.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict//stderr/bc2enhancer_ke2018-rna-dna-norm-br3.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 2.bc2enhancer_dnabc-Bkgd_norm.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict// ../../../data/otxa-sequencing-data/bc-enhancer-dictionaries/_dicts/MLOTX-wei-dicts/MLOTXA-wei-dict// 1 2 1 1 4 bc2enhancer_ke2018-rna-dna-norm-br3