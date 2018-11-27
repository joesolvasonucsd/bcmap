# Purpose: splits collapsed unique reads/counts file for parallele seq2dict.py processing

# Usage: bash collapsed2dict.sh <dir/to/data> </dir/to/data/input_file> <email> <memory_per_job> <hours_per_job>
#
# Where:
#	<dir/to/data>	 		location of data
#	<dir/to/data/input_file>	directory and fileName of collapsed unique/counts file to convert to dict
#	<email>				user email
#	<memory_per_job>		memory allocation request per job submitted to sdsc (integer in gigs)
#	<hours_per_job> 		max walltime request per job submitted to sdsc (integer in hours)

DATADIR=$1
INPUTFILE_LOC=$2

EMAIL=$3
MEM=$4
HOURS=$5

# split merged read count file && submit all split files for batch analysis
python 2.split4parallele.py $DATADIR $INPUTFILE_LOC && python 3.sbatch_seq2dict_v2.4.py $INPUTFILE_LOC $EMAIL $MEM $HOURS
cp 2.split4parallele.py 3.sbatch_seq2dict_v2.4.py ${DATADIR}scripts/
