#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=findMotifs_otxa-rss-i6
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --mem=96G
#SBATCH --time=48:00:00
#SBATCH --output=../../../data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stdout/findMotifs_otxa-rss-i6.out.txt
#SBATCH --error=../../../data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//stderr/findMotifs_otxa-rss-i6.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
module load homer/4.9_2-20-2017
bash findMotifs-wei.sh ../../../data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/bc2enhancer_otxa-rss-i6_enhancers_greater_4.0.fa ../../../data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6/allEnhancerInDNALibrary_u.fa ../../../data/otxa-sequencing-data/otxa-rss-library-screens/rnaseq-normal-library-science-2015/otxa-rss-i6//motif-output/ 12