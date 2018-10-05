# Purpose: Produce a tab-separated-values file with column 1 = Read and column 2 = Read Counts. All reads in this file are unique. 

# Usage: 
#       bash reads2BcDict.sh <data directory*> <basename> <email>

# Notes:
#       * NOTE ensure <data directory> ends with '/'

# Log (<basename>.log) file of analysis printed to same directory as data

# Tested 181003

# Input: One or more .fastq files with a common basename. If only one file, basename can be the name except the .fastq suffix (for example: sample1.fastq basename would be sample1)
# Outputs: 
#       1. <basename>_collapsed.fastq - all .fastq files used in analyses concatenated
#       2. <basename>_collapsed_filtered.fastq - filters out N containing reads from _collapsed.fastq
#       3. <basename>_collapsed_filtered_collapsed.txt - tsv file containing unique reads: column 1 = read and column 2 = read count.

# script meant to be run from current directory (/scripts/)

# script called declaring the following (order of arguments must be retained):
# bash reads2BcDict.sh <data directory> <basename of input files> 



####################
# Script 
####################

# email 
EMAIL=$3

# Where python scripts are located
SCRIPTSDIR="/oasis/projects/nsf/csd579/solvason/scripts/bcmap/DNA_library/"

# Where can your data be found
DATADIR=$1

# basename = common part of sequence file name. For example: basename(sample1_index1.fastq & sample1_index2.fastq) = sample1
BASENAME=${DATADIR}$2
CONCATENATED_BASENAME=${BASENAME}_collapsed
QFILTERED_BASENAME=${CONCATENATED_BASENAME}_filtered
COLLAPSED_BASENAME=${QFILTERED_BASENAME}_collapsed.txt

# log files
LOG=${BASENAME}.txt
READCOUNTS=${BASENAME}_counts.tsv

touch $LOG $READCOUNTS


# Process the DNA dictionary data:
echo "Unizpping gz files..."
zcat ${BASENAME}*.gz > ${CONCATENATED_BASENAME}.fastq # unzipping the files and concatenate to single .fastq

echo "Quality filtering..."
cat ${CONCATENATED_BASENAME}.fastq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_BASENAME}.fastq # Filter on quality score to remove low quality reads

echo "Deduping reads..."
python ${SCRIPTSDIR}1.collapseSeq.py ${QFILTERED_BASENAME}.fastq # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file

# combine reads here if you need to, but another script is needed

echo "Splitting for parallele..."
python ${SCRIPTSDIR}2.split4parallele.py ${COLLAPSED_BASENAME} # Script 2 splits the data into smaller files (10,000 reads per file)

# Count reads at various steps

echo "Counting Reads..."
echo -e "$(wc -l < ${CONCATENATED_BASENAME}.fastq)\t${CONCATENATED_BASENAME}.fastq" >> $READCOUNTS # reads analyzed
echo -e "$(wc -l < ${QFILTERED_BASENAME}.fastq)\t${QFILTERED_BASENAME}.fastq" >> $READCOUNTS # reads not containing N
echo -e "$(wc -l < ${COLLAPSED_BASENAME})\t${COLLAPSED_BASENAME}" >> $READCOUNTS # reads unique

echo "Submitting for sbatch..."
python ${SCRIPTSDIR}3.sbatch.py $DATADIR $BASENAME $EMAIL # has all the information to run the last part of the code seq2dict_v2.4

#8.The script seq2.dict_v2.4.py is for the Fn library, seq2.dict_v2.4_inverse.py is for Fi libraries # This script makes the library of enhancer and bc into the dictionary 

#How to process RNA/DNAbc data

#9.gunzip  BASENAME*.gz # unzipping the files

#10.Cat BASENAME*.fastq > file_name*.fastaq # Merges all data with the same index 

#11.cat input.fq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > file_name_filtered.fq # Filter on quality score to remove low quality reads

#12.Python collapseseq.py <file_name_filtered.fq> # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file

#13.Python combinecollapsefiles.py file_name_collapse.txt # Script 1.5.  Combines all the reads that are the same sequence. 

#14.Python RNAseq2reads.py <full path file output of previous script is input for this> # Script 2. Identifies each barcode and associates with number of reads. 

#15.Python barcode2enh.py  # Script 3. This calls the files so no need to put an input. Associates the barcode with the enhancer and lists number of reads found. 


#Your folder must contain the DNA folder - with dictionary and RNA folder. Script file names will have to be changed to match your analysis. 

#Should take ~4-8hrs to run through this. 


#Notes:
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
#'''
