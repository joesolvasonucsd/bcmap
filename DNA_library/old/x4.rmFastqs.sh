# Purpose: Delete all intermediate files (.fastq files) in a given directory

# Usage: bash x4.rmFastqs.sh <dir/to/data/>

# Where:
#       <dir/to/data/>     directory and filename of input file

DATADIR=$1

rm ${DATADIR}*.fastq
