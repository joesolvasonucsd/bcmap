findMotifs.pl RNA/enhancers_cut4anyFn23_20150110.fa fasta motif_output/enhancers_highExp_cut4anyFn23_vs_DNA_20150110_6to8bp_opt/ -fasta RNA/allEnhancerInDNALibrary_u.fa -len 6,7,8 -p 12 -nlen 0 -noweight -noknown


# instructions http://homer.salk.edu/homer/microarray/index.html

# findMotifs.pl #findMotif program
# RNA/enhancers_cut4anyFn23_20150110.fa #forground
# fasta #fasta format
# motif_output/enhancers_highExp_cut4anyFn23_vs_DNA_20150110_6to8bp_opt/ # output directory
# -fasta #fasta format
# RNA/allEnhancerInDNALibrary_u.fa #background
# -len 6,7,8 #length of motifs
# -p 12 #use 12 CPUs 
# -nlen 0 # disable normalization by k-mers
# -noweight # disable normalization by %CpG
# -noknown # don't check the known motifs

# -opt <a file of position weight matrix> # optimize position weight matrices
