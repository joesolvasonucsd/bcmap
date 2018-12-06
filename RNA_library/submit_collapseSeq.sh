#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=collapseSeq_KO_DNAbc_BR_2
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=20G
#SBATCH --time=1:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict/stdout/collapseSeq_KO_DNAbc_BR_2.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict/stderr/collapseSeq_KO_DNAbc_BR_2.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash A.reads2collapsed.sh /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/data/ /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict/ KO_DNAbc_BR_2