#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=RNAseq2reads:bc2enhancer_otxa-rss-i6
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=2:00:00
#SBATCH --output=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stdout/bc2enhancer_otxa-rss-i6.out.txt
#SBATCH --error=/oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stderr/bc2enhancer_otxa-rss-i6.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load scipy
module load biopython
python 2.barcode2enhancer_v3_joe.py /oasis/projects/nsf/csd579/solvason/data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6// ../../../data/otxa-sequencing-data/bc-enhancer-dictionaries/_dicts/MLOTXA-dict// 1 4 bc2enhancer_otxa-rss-i6