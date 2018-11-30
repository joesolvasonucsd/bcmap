# Purpose: Collapse to unique reads and record read counts.

# Usage: bash A.reads2collapsed.sh <dir/to/input/data/> </dir/to/output> <basename_gz>

# Where:
#       <data_directory>        directory where input gzipped read files are located
#       <basename>              common filename of gzipped fastq files


############
# Script
############

# Arguments
DATADIR=$1
OUTPUTDIR=$2
BASENAME_INPUT=${DATADIR}/$3
BASENAME_OUTPUT=${OUTPUTDIR}/$3

# File Names
QFILTERED_BASENAME=${BASENAME_OUTPUT}_collapsed_filtered

# Unzip all gz files with same basename | QC filter | save filtered.fastq
zcat  ${BASENAME_INPUT}*.fastq.gz |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_BASENAME}.fastq

# Count & Deduplicate reads
python 0.collapseSeq.py ${QFILTERED_BASENAME}.fastq
