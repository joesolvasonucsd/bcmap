# Usage
#	bash 2.findMotifs-wei.sh <fasta_foreground> <fasta_background> </dir/to/output/> <cpus_requested>












FOREGROUND=$1
BACKGROUND=$2
OUTPUTDIR=$3
CPUS=$4

findMotifs.pl $FOREGROUND fasta $OUTPUTDIR -fasta $BACKGROUND -len 6,7,8 -p $CPUS -nlen 0 -noweight -noknown


# instructions http://homer.salk.edu/homer/microarray/index.html

# findMotifs.pl #findMotif program
# $FOREGROUND #forground
# fasta # fasta format
# $OUTPUTDIR # output directory
# -fasta #fasta format
# $BACKGROUND #background
# -len 6,7,8 #length of motifs
# -p $CPUS #use 12 CPUs
# -nlen 0 # disable normalization by k-mers
# -noweight # disable normalization by %CpG
# -noknown # don't check the known motifs

# -opt <a file of position weight matrix> # optimize position weight matrices
