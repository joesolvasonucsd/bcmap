#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=findMotifs_ke2018-rna-dna-weidict
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem=96G
#SBATCH --time=2:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict//stdout/findMotifs_ke2018-rna-dna-weidict.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict//stderr/findMotifs_ke2018-rna-dna-weidict.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
bash 2.findMotifs-wei.sh /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict/bc2enhancer_ke2018-rna-dna_enhancers_greater_4.0.fa /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict/all-enhancers-dnabc-bc_u.fa /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/library-screens/ke-2018-rnaseq-dnaseq/rnabc-dnabc-br2_1-weidict//motif-output/ 12