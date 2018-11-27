#!/bin/bash
#SBATCH --partition=vector
#SBATCH --qos=vector_batch
#SBATCH --job-name=findMotifs
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12 # number of CPUs
#SBATCH --mem=96G # memory
#SBATCH --time=199:00:00
#SBATCH --output=findMotifs.out.txt
#SBATCH --error=findMotifs.err.txt
#SBATCH --export=ALL
#SBATCH --mail-user=wzhang1984@berkeley.edu # email
#SBATCH --mail-type=ALL

findMotifs.pl RNA/enhancers_cut4anyFn23_20150110.fa fasta motif_output/enhancers_highExp_cut4anyFn23_vs_DNA_20150110_6to8bp_opt/ -fasta RNA/allEnhancerInDNALibrary_u.fa -len 6,7,8 -p 12 -nlen 0 -noweight -noknown
