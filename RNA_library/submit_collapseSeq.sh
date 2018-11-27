#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=collapseSeq_MLOTXAFiBR1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=15G
#SBATCH --time=2:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/stdout/collapseSeq_MLOTXAFiBR1.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/stderr/collapseSeq_MLOTXAFiBR1.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
bash A.reads2collapsed.sh /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/ MLOTXAFiBR1