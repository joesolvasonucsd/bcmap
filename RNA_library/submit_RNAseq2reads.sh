#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:ke2018-rna-dna-norm-br3
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=4:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict//stdout/ke2018-rna-dna-norm-br3.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict//stderr/ke2018-rna-dna-norm-br3.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 1.RNAseq2reads.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict// /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict/KO_DNAbc_BR_3_collapsed_filtered_collapsed.txt /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-norm-br3-weidict/KO_RNA-BR2_3_collapsed_filtered_collapsed.txt