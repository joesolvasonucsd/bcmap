#!/bin/bash
#SBATCH --partition=shared
#SBATCH --job-name=mergeFiles_../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/30KLibrary1_collapsed_filtered_collapsed.txt_../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/30KLibrary2_collapsed_filtered_collapsed.txt
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=24:00:00
#SBATCH --output=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/stdout/30KLibrary.out.txt
#SBATCH --error=../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/stderr/30KLibrary.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=solvason@ucsd.edu
#SBATCH --mail-type=ALL
module load python
python 1.5.combineCollapsedFiles.py ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/ 30KLibrary ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/30KLibrary1_collapsed_filtered_collapsed.txt ../../../data/otxa-sequencing-data/enhancer-bc-mapping-dna-dict-data/30KLibrary/30KLibrary2_collapsed_filtered_collapsed.txt