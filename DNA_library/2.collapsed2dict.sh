# Purpose: splits collapsed unique reads/counts file for parallele seq2dict.py processing

# Usage: bash collapsed2dict.sh <seq2dict_script_variant> <dir/to/data> </dir/to/data/input_file> <email> <memory_per_job> <hours_per_job> <scripts_dir>
#
# Where:
#	<dir/to/data>	 		location of data
#	<dir/to/data/input_file>	directory and fileName of collapsed unique/counts file to convert to dict
#	<scripts_dir>			directory where DNA_library scripts are

SCRIPTDIR=$7
SEQ2DICT=$1
DATADIR=$2
INPUTFILE_LOC=$3

EMAIL=$4
MEM=$5
HOURS=$6

# split merged read count file && submit all split files for batch analysis
python ${SCRIPTDIR}2.split4parallele.py $DATADIR $INPUTFILE_LOC && python ${SCRIPTDIR}3.sbatch.py $SEQ2DICT $INPUTFILE_LOC $EMAIL $MEM $HOURS $SCRIPTDIR
