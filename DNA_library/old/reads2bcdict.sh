#!/bin/bash
# Purpose: Produce a tab-separated-values file with column 1 = Read and column 2 = Read Counts. All reads in this file are unique. 

# Usage: bash reads2BcDict.sh <data_directory> <basename> <email> <memory_per_job> <hours_per_job>
# 	Where:
#		<data_directory>	directory where input gzipped read files are located
#		<basename>		common filename of gzipped read files
#		<email>			user email
#		<memory_per_job>	(eg 4G for 4 gigs) amount of memory allocated to each seq2dict.py job
#               <hours_per_job>         (integer) number of hours requested for job

# Input:
#	One or more .fastq files with a common basename. If only one file, basename can be the name except the .fastq suffix (for example: sample1.fastq basename would be sample1)
# Outputs:
#       1. <basename>_collapsed.fastq - all .fastq files used in analyses concatenated
#       2. <basename>_collapsed_filtered.fastq - filters out N containing reads from _collapsed.fastq
#       3. <basename>_collapsed_filtered_collapsed.txt - tsv file containing unique reads: column 1 = read and column 2 = read count.

# script meant to be run from current directory (/scripts/)

# script called declaring the following (order of arguments must be retained):
# bash reads2BcDict.sh <data directory> <basename of input files>

# Exit if user provided no arguments
if [ -z $1 ]
then
	echo "Error: No arguments provided for reads2BcDict.sh. Exiting"
	exit
fi

# Exit if command fails
set -e

####################
# Script
####################

EMAIL=$3
MEMORY=$4
JOBHOURS=$5

# Where can your data be found
DATADIR=$1

# basename = common part of sequence file name. For example: basename(sample1_index1.fastq & sample1_index2.fastq) = sample1
BASENAME=${DATADIR}$2
CONCATENATED_BASENAME=${BASENAME}_collapsed
QFILTERED_BASENAME=${CONCATENATED_BASENAME}_filtered
COLLAPSED_BASENAME=${QFILTERED_BASENAME}_collapsed

# read counts
READCOUNTS=${BASENAME}_counts.tsv
FILESIZES=${BASENAME}_fileSizes.tsv

touch $READCOUNTS $FILESIZES


# Process the DNA dictionary data:
echo "Unizpping gz files..."
zcat ${BASENAME}*.gz > ${CONCATENATED_BASENAME}.fastq # unzipping the files and concatenate to single .fastq

echo "Quality filtering..."
cat ${CONCATENATED_BASENAME}.fastq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_BASENAME}.fastq # Filter on quality score to remove low quality reads

echo "Deduping reads..."
python 1.collapseSeq.py ${QFILTERED_BASENAME}.fastq # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file

# combine reads here if you need to, but another script is needed

echo "Splitting for parallel..."
python 2.split4parallele.py ${COLLAPSED_BASENAME}.txt # Script 2 splits the data into smaller files (10,000 reads per file)

# Count reads at various steps

echo "Counting Reads..."
echo -e "$(expr $(wc -l < ${CONCATENATED_BASENAME}.fastq) / 4)\t${CONCATENATED_BASENAME}.fastq" >> $READCOUNTS # reads analyzed
echo -e "$(expr $(wc -l < ${QFILTERED_BASENAME}.fastq) / 4)\t${QFILTERED_BASENAME}.fastq" >> $READCOUNTS # reads not containing N
echo -e "$(expr $(wc -l < ${COLLAPSED_BASENAME}.txt) / 1)\t${COLLAPSED_BASENAME}.txt" >> $READCOUNTS # reads unique

echo "Calculating File Sizes..."
echo -e "$(du -sh ${CONCATENATED_BASENAME}.fastq)\t${CONCATENATED_BASENAME}.fastq" >> $FILESIZES # file size of uncollapsed fastq file
echo -e "$(du -sh ${QFILTERED_BASENAME}.fastq)\t${QFILTERED_BASENAME}.fastq" >> $FILESIZES # file size of qc reads
echo -e "$(du -sh ${COLLAPSED_BASENAME}.txt)\t${COLLAPSED_BASENAME}.txt" >> $FILESIZES # file size of unique reads

echo "Deleting Intermediate Files..."
rm ${DATADIR}*.fastq

echo "Submitting for sbatch..."
python 3.sbatch.py $DATADIR ${COLLAPSED_BASENAME} $BASENAME $EMAIL $MEMORY $JOBHOURS # has all the information to run the last part of the code seq2dict_v2.4


################################
# Notes on regular Expressions #
################################

#1. What does command line in 3 mean:
#I asked Wei to explain the command for 3, he said the following
#
#'^@.* [^:]*:N:[^:]*:'
#
#This is the regular expression to parse the header line, not the sequence themselves. As far as I can remember, the header line starts with a "@", and ":N:" indicates that the sequence passes the quality control. I recommend Josh to read some online documents about "regular expression" (such as its Wikipedia page). It will start to make sense if you have a better understanding of regular expression.
#
#grep -A <int> considers 1+<int> lines at a time (if <int>=3, 4 lines would be considered at a time. A read takes up 4 lines of a fastq file) 
#
#grep -v
#
#These are the options for the linux command "grep". Again, you can refer to the related online documents.
#
#2. Server
#The server we use is called comet, and is part of UCSD super computer service. We can use other servers if you think they would be better.  http://www.sdsc.edu/support/user_guides/comet.html 
#
