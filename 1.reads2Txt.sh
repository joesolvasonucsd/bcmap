#!/bin/bash

# Purpose: Produce a tab-separated-values file with column 1 = Read and column 2 = Read Counts. All reads in this file are unique. 

# Usage: 
#	bash 1.reads2Txt.sh <data directory> <basename>




# Input: One or more .fastq files with a common basename. If only one file, basename can be the name except the .fastq suffix (for example: sample1.fastq basename would be sample1)
# Outputs: 
#	1. <basename>_collapsed.fastq - all .fastq files used in analyses concatenated
#	2. <basename>_collapsed_filtered.fastq - filters out N containing reads from _collapsed.fastq
#	3. <basename>_collapsed_filtered_collapsed.txt - tsv file containing unique reads: column 1 = read and column 2 = read count.

# script meant to be run from current directory (/scripts/)

# script called declaring the following (order of arguments must be retained):
# bash reads2BcDict.sh <data directory> <basename of input files> 



####################
# Script 
####################

# Where can your data be found
DATADIR=$1

# basename = common part of sequence file name. For example: basename(sample1_index1.fastq & sample1_index2.fastq) = sample1
BASENAME=${DATADIR}$2
CONCATENATED_BASENAME=${BASENAME}_collapsed
QFILTERED_BASENAME=${CONCATENATED_BASENAME}_filtered
COLLAPSED_BASENAME=${QFILTERED_BASENAME}_collapsed.txt


#How to process the DNA dictionary data:
gunzip  ${BASENAME}*.gz # unzipping the files

cat ${BASENAME}*.fastq > ${CONCATENATED_BASENAME}.fastq # concatenates all sequencing files with common basename to <basename>_collapsed.fastq

cat ${CONCATENATED_BASENAME}.fastq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_BASENAME}.fastq # Filter on quality score to remove low quality reads

python 1.collapseSeq.py ${QFILTERED_BASENAME}.fastq # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file


