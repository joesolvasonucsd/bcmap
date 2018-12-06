
# Usage: bash reads_preprocessing <data_directory> <basename> <scripts_dir>

#	Where...
#		<data_directory> 	directory containing data. MUST END IN '/'!!!!
#		<basename>		shared filename of all input files
#		<scripts_dir>		directory where DNA_library is located

SCRIPTSDIR=$3

DATADIR=$1
BASENAME=$2

INPUT_LOC=${DATADIR}${BASENAME}

CONCATENATED_LOC=${INPUT_LOC}_collapsed
QFILTERED_LOC=${CONCATENATED_LOC}_filtered

# Process the DNA dictionary data:
echo "Unizpping multiple .fastq.gz to a single concatenated .fastq..."
zcat ${INPUT_LOC}*.gz > ${CONCATENATED_LOC}.fastq # unzipping the files and concatenate to single .fastq

echo "Quality filtering..."
cat ${CONCATENATED_LOC}.fastq |  grep -A 3 '^@.* [^:]*:N:[^:]*:' | grep -v "^--$" > ${QFILTERED_LOC}.fastq # Filter on quality score to remove low quality reads

echo "Removing duplicate reads..."
python ${SCRIPTSDIR}1.collapseSeq.py ${QFILTERED_LOC}.fastq # Script 1. Strips data down to the read and counts per read. This outputs collapsed.txt file
cp ${SCRIPTSDIR}1.collapseSeq.py ${DATADIR}scripts/
