#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:otxa-rss-i6
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=12:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stdout/otxa-rss-i6.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stderr/otxa-rss-i6.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 1.RNAseq2reads.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6// /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/MLOTXAFiBR1_collapsed_filtered_collapsed.txt