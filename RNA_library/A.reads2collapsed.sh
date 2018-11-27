# Purpose: Collapse to unique reads and record read counts.

# Usage: bash reads2counts.sh <dir/to/data/> <basename_gz>

# Where:
#       <data_directory>        directory where input gzipped read files are located
#       <basename>              common filename of gzipped fastq files


############
# Script
############

# Arguments
DATADIR=$1
BASENAME=${DATADIR}/$2

# Useful Vars
CONCATENATED_BASENAME=${BASENAME}_collapsed
QFILTERED_BASENAME=${BASENAME}_collapsed_filtered
COLLAPSED_BASENAME=${BASENAME}_collapsed_filtered_collapsed

# Unzip all fastq files to single file
zcat  ${BASENAME}*.fastq.gz > ${CONCATENATED_BASENAME}.fastq

# Quality filter
cat ${CONCATENATED_BASENAME}.fastq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_BASENAME}.fastq

# Count & Deduplicate reads
python 1.collapseSeq.py ${QFILTERED_BASENAME}.fastq
